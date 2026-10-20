from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # Vérifie que la connexion est vivante avant de l'utiliser
    pool_recycle=3600,    # Recrée les connexions toutes les heures
    pool_size=10,
    max_overflow=200,
    echo=False,           # Mettre True en dev pour voir les requêtes SQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()