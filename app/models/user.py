from sqlalchemy import Column, String, Boolean, DateTime, func, SmallInteger
from sqlalchemy.orm import relationship

from app import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    # --- Identity ---
    id_account = Column(String(191), primary_key=True)
    email = Column(String(191), unique=True, index=True, nullable=False)
    hashed_password = Column(String(191), nullable=False)

    # --- Profile ---
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    # --- States ---
    admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # --- Sécurité ---
    failed_login_attempts = Column(SmallInteger, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime(timezone=True), nullable=True)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # --- Relationships ---
    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan", order_by="Document.created_at.desc()"
)