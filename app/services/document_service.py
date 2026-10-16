from datetime import datetime
import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models import Document
from schemas.document import DocumentCreate

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}

class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, document_id: int) -> Document | None:
        return self.db.query(Document).filter(Document.id_document == document_id).first()

    def create_from_upload(self, file: UploadFile, data: DocumentCreate, owner_id: int) -> Document:

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise ValueError("Invalid file type.")

        if not file.filename:
            raise ValueError("No file selected")

        """
        Sauvegarde le fichier physique et crée l'entrée en base.
        """
        # 1. Générer un nom unique pour éviter les conflits
        # On garde l'extension originale
        file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

        timestamp = datetime.now().strftime("%Y/%m")
        folder_path = os.path.join("uploads", timestamp)
        full_path = os.path.join(folder_path, unique_filename)

        os.makedirs(folder_path, exist_ok=True)

        with open(full_path, "wb") as buffer:
            while chunk := file.file.read(8192):
                buffer.write(chunk)

        db_doc = Document(
            id_account=owner_id,
            title=data.title,
            description=data.description,
            school_year=data.school_year,
            sector=data.sector,
            sector_year=data.sector_year,
            session=data.session,
            file_path=full_path,
            content_type=file.content_type or "application/octet-stream",
            file_size= 0 if file.size is None else file.size,
        )

        self.db.add(db_doc)
        self.db.commit()
        self.db.refresh(db_doc)
        return db_doc