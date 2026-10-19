import datetime
from typing import Optional
from pydantic import Field
from schemas.base import CamelModel

class DocumentBase(CamelModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    subject: str = Field(min_length=1, max_length=255)
    sector: str = Field(..., min_length=1, max_length=100)
    sector_year: int = Field(..., ge=1, le=5)
    school_year: int = Field(..., ge=2000, le=2100)
    session: Optional[int] = None
    format: str = Field(min_length=1, max_length=100)
    created_at: datetime.datetime


class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: str = Field(validation_alias="id_document", serialization_alias="id")
    author: str = Field(validation_alias="id_account", serialization_alias="author")
    content_type: str
    size: int = Field(validation_alias="file_size", serialization_alias="size")
    viewed_at: datetime.datetime | None

class DocumentQuery(CamelModel):
    page: int = Field(1, ge=1)
    title: str | None = None
    subject: str | None = None
    format: str | None = None
    page_size: int = Field(10, ge=1, le=100)

class DocumentQueryResponse(CamelModel):
    data: list[DocumentResponse] = Field(default_factory=list)
    total: int