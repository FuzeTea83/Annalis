from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String

from app import Base


class UserView(Base):
    __tablename__ = "user_views"
    __table_args__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    #--- Identity ---
    id = Column(Integer, primary_key=True, autoincrement=True)


    # --- Timestamps ---
    viewed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # --- Foreign Keys ---
    document_id = Column(String(191), ForeignKey("documents.id_document", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(191), ForeignKey("users.id_account", ondelete="CASCADE"), nullable=False)
