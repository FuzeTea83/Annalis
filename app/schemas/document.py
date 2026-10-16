import datetime
from typing import Optional
from pydantic import Field
from datetime import datetime
from schemas.base import CamelModel


class DocumentBase(CamelModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    created_at: type[datetime]
    content_type: str = Field(..., min_length=1, max_length=100)
    subject: str = Field(min_length=1, max_length=255)
    sector: str = Field(..., min_length=1, max_length=100)
    sector_year: int = Field(..., ge=1, le=5)
    school_year: int = Field(..., ge=2000, le=2100)
    session: Optional[int] = None


class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(CamelModel):
    id: int
    owner_id: int
    title: str
    description: Optional[str] = None
    annee_scolaire: int
    filiere: str
    session: Optional[str] = None
    file_name: str
    file_path: str
    content_type: str
    file_size: int
    is_public: bool
    created_at: type[datetime]
    updated_at: Optional[type[datetime]] = None

class DocumentQuery(DocumentBase):
    title: str | None = None
    content: str | None = None