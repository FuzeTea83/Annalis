from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Form, status, Query
from sqlalchemy.orm import Session

from app import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas import DocumentCreate, DocumentQuery, DocumentQueryResponse, DocumentResponse
from app.services import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
        file: UploadFile = File(...),
        title: str = Form(...),
        description: str = Form(None),
        subject: str = Form(...),
        sector: str = Form(...),
        sector_year: int = Form(...),
        school_year: int = Form(...),
        session: int = Form(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    data = DocumentCreate(
        title=title,
        description=description,
        subject=subject,
        sector=sector,
        sector_year=sector_year,
        school_year=school_year,
        session=session,
        format=file.content_type.split("/")[-1] if file.content_type else "unknown"
    )

    service = DocumentService(db)
    document = service.create_from_upload(file, data, current_user)
    return service.build_document_response_single(document)

@router.get("/recent", status_code=status.HTTP_200_OK, response_model=DocumentQueryResponse)
def get_recent_documents(limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = DocumentService(db)
    documents, total = service.get_recent_views(current_user, limit)
    return service.build_document_response_multiple(documents, total)


@router.get("/view", status_code=status.HTTP_200_OK, response_model=DocumentQueryResponse)
def get_document(
        page: int = Query(default=1),
        title: str = Query(None),
        subject: str = Query(None),
        format: str = Query(None),
        page_size: int = Query(default=10),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    query = DocumentQuery(
        page=page,
        title=title,
        subject=subject,
        format=format,
        page_size=page_size
    )

    service = DocumentService(db)
    documents, total = service.get_documents(query)
    return service.build_document_response_multiple(documents, total)

@router.get("/{doc_id}/download", status_code=status.HTTP_200_OK)
def download_document(doc_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print(f"route /download/{doc_id}")
    service = DocumentService(db)
    document = service.get_document(doc_id)
    service.record_view(document, current_user)
    return service.build_file_download_response(document)

@router.get("/{doc_id}/preview", status_code=status.HTTP_200_OK)
def preview_document(doc_id: str, db: Annotated[Session, Depends(get_db)], current_user: User = Depends(get_current_user)):
    print(f"route /preview_test/{doc_id}")
    service = DocumentService(db)
    document = service.get_document(doc_id)
    service.record_view(document, current_user)
    return service.build_file_preview_response(document)


