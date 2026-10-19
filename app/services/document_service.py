import os
import uuid
from datetime import datetime
from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse
from fastapi.responses import FileResponse
from urllib.parse import quote

from app.core.exeptions import InvalidFileTypeError, UnknownFileError, FileTooLargeError, DocumentNotFoundError
from app.models import Document, User, UserView
from app.schemas import DocumentCreate, DocumentQueryResponse, DocumentResponse, DocumentQuery
from app.services import user_service

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}

FILE_SIZE_LIMIT_MB = 10
DOCUMENT_FOLDER = "documents"



class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, document_id: str) -> Document | None:
        return self.db.query(Document).filter(Document.id_document == document_id).first()

    def get_author_name(self, document: Document) -> str:
        service = user_service.UserService(self.db)
        user = service.get_by_id(document.id_account)
        return f"{user.first_name} {user.last_name}" if user else "Unknown"

    def get_viewed_at(self, document: Document, user_id: str) -> datetime | None:
        return self.db.query(UserView.viewed_at).filter(
            UserView.document_id == document.id_document,
            UserView.user_id == user_id
        ).scalar()

    def create_from_upload(self, file: UploadFile, data: DocumentCreate, current_user: User) -> Document:
        """
        Crée un document à partir d'un fichier téléchargé et des données associées.
        """
        if not file.filename:
            raise UnknownFileError

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise InvalidFileTypeError

        if file.size is not None and file.size > FILE_SIZE_LIMIT_MB * 1024 * 1024:
            raise FileTooLargeError(FILE_SIZE_LIMIT_MB)


        file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

        timestamp = datetime.now().strftime("%Y/%m")
        folder_path = os.path.join(DOCUMENT_FOLDER, timestamp)
        full_path = os.path.join(folder_path, unique_filename)

        os.makedirs(folder_path, exist_ok=True)

        with open(full_path, "wb") as buffer:
            while chunk := file.file.read(8192):
                buffer.write(chunk)

        doc = Document(
            id_document=str(uuid.uuid4()),
            id_account=current_user.id_account,
            title=data.title,
            description=data.description if data.description else "",
            subject=data.subject,
            school_year=data.school_year,
            sector=data.sector,
            sector_year=data.sector_year,
            format=data.format,
            session=data.session,
            file_path=full_path,
            content_type=file.content_type or "application/octet-stream",
            file_size= 0 if file.size is None else file.size,
        )

        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def get_document(self, doc_id: str) -> Document:
        """
        Récupère un document par son ID et vérifie que le fichier existe.
        """
        document = self.get_by_id(doc_id)
        if not document:
            raise DocumentNotFoundError

        if not os.path.exists(document.file_path):
            raise DocumentNotFoundError

        return document

    def build_file_download_response(self, document: Document) -> FileResponse:
        """
        Crée une réponse de fichier pour le téléchargement ou l'affichage du document.
        """
        return FileResponse(
            path=document.file_path,
            filename=document.title,
            media_type=document.content_type
        )

    def build_file_preview_response(self, document: Document) -> StreamingResponse:
        """
        Crée une réponse de fichier pour le téléchargement ou l'affichage du document.
        """
        def iterfile():
            with open(document.file_path, "rb") as f:
                while chunk := f.read(8192):
                    yield chunk

        safe_title = quote(document.title)
        return StreamingResponse(
            iterfile(),
            media_type=document.content_type,
            headers={
                "Content-Disposition": f"inline; filename*=UTF-8''{safe_title}",
                "Accept-Ranges": "bytes",
            },
        )


    def record_view(self, document: Document, current_user: User) -> None:
        """
        Enregistre qu'un utilisateur a consulté un document.
        """
        view = self.db.query(UserView).filter_by(document_id=document.id_document, user_id=current_user.id_account).first()
        if view:
            view.viewed_at = datetime.now()
            self.db.commit()
            self.db.refresh(view)
            return

        view = UserView(
            document_id=document.id_document,
            user_id=current_user.id_account,
        )
        self.db.add(view)
        self.db.commit()

    def get_recent_views(self, current_user: User, limit: int = 10) -> tuple[list[Document], int]:
        """
        Récupère les documents consultés récemment par l'utilisateur.
        """
        query = (
            self.db.query(Document)
            .join(UserView, UserView.document_id == Document.id_document)
            .filter(UserView.user_id == current_user.id_account)
            .order_by(UserView.viewed_at.desc())
            .limit(limit)
        )
        total = query.count()
        return query.all(), total

    def get_documents(self, query: DocumentQuery) -> tuple[list[Document], int]:
        """
        Récupère une liste de documents en fonction des critères de recherche.
        """
        documents = self.db.query(Document)
        if query.subject:
            documents = documents.filter(Document.subject == query.subject)
        if query.title:
            documents = documents.filter(Document.title.ilike(f"%{query.title}%"))
        if query.format:
            documents = documents.filter(Document.content_type.ilike(f"%{query.format}%"))
        if query.page:
            offset = (query.page - 1) * query.page_size
            documents = documents.offset(offset).limit(query.page_size)
        total = documents.count()
        return documents.all(), total

    def build_document_response_single(self, document: Document) -> DocumentResponse:
        """
        Construit une réponse de requête à partir d'un document.
        """
        return DocumentResponse(
                id=document.id_document,
                author=self.get_author_name(document),
                content_type=document.content_type,
                size=document.file_size,
                title=document.title,
                description=document.description,
                created_at=document.created_at,
                subject=document.subject,
                sector=document.sector,
                sector_year=document.sector_year,
                school_year=document.school_year,
                session=document.session,
                format=document.format,
                viewed_at=self.get_viewed_at(document, document.id_account)
        )

    def build_document_response_multiple(self, documents: list[Document], total: int) -> DocumentQueryResponse:
        """
        Construit une réponse de requête de documents à partir d'une liste de documents.
        """
        return DocumentQueryResponse(
            data=[self.build_document_response_single(document) for document in documents],
            total=total
        )