import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database import get_db
from models import User, Document
from schemas.document import DocumentCreate
from schemas.document import DocumentResponse
from services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED, responses={
    201: {"description": "Document uploaded successfully"},
    400: {"description": "Invalid file type or no file selected"},
})
def upload_document(
        file: UploadFile = File(...),
        title: str = Form(...),
        description: str = Form(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    data = DocumentCreate(
        title=title,
        description=description,
    )

    service = DocumentService(db)
    try:
        return service.create_from_upload(file, data, current_user.id_account)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{doc_id}", response_model=DocumentResponse, responses={404: {"description": "Document not found"}})
def get_document(doc_id: int, db:  Annotated[Session, Depends(get_db)]):
    doc = db.get(Document, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.get("/download/{doc_id}", responses={404: {"description": "Document not found"}})
def download_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    from fastapi.responses import FileResponse

    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404,
                            detail="File does not exist")  # TODO: Log this error for further investigation

    return FileResponse(
        path=doc.file_path,
        filename=doc.title,
        media_type=doc.content_type
    )
