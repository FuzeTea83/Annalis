from sqlalchemy import (Column, Integer, String, SmallInteger, ForeignKey, Text, DateTime, func)
from sqlalchemy.orm import relationship

from app import Base


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    #--- Identity ---
    id_document = Column(Integer, primary_key=True, autoincrement=True)
    id_account = Column(Integer, ForeignKey("users.id_account", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # --- File Storage ---
    file_path = Column(String(500), nullable=False)
    content_type = Column(String(100), nullable=False)

    # --- File Metadata ---
    file_size = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # --- Document Metadata ---
    subject = Column(String(255), nullable=False)
    sector = Column(String(100), nullable=False)
    sector_year = Column(SmallInteger, nullable=False)
    school_year = Column("school_year", SmallInteger, nullable=False)
    session = Column("session", SmallInteger, nullable=False)

    # --- Relationships ---
    owner = relationship("User", back_populates="documents")

    def __repr__(self):
        return f"<Document {self.id_document}: {self.title}>"