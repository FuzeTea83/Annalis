#import mimetypes
#import os
#import secrets
#from pathlib import Path
#from urllib.parse import quote
#
#import bcrypt
#import jwt
#from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, Query, UploadFile
#from fastapi.middleware.cors import CORSMiddleware
#from fastapi.responses import FileResponse, JSONResponse
#from sqlalchemy import func, or_, select
#from sqlalchemy.orm import Session, joinedload
#
#from app.database import Base, engine, get_db
#from app.models import Document, User
#from app.schemas import AuthResponse, Credentials, RegisterPayload, UserResponse
#
#BASE_DIR = Path(__file__).resolve().parent.parent
#UPLOAD_DIR = BASE_DIR / "uploads"
#UPLOAD_DIR.mkdir(exist_ok=True)
#JWT_SECRET = os.getenv("JWT_SECRET", "change-this-secret-in-production")
#ALLOWED_EXTENSIONS = {".pdf": "PDF", ".docx": "DOCX", ".pptx": "PPTX"}
#MAX_FILE_SIZE = 20 * 1024 * 1024
#
#app = FastAPI(title="Annalis API", version="1.0.0")
#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(","),
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)
#
#
#@app.on_event("startup")
#def create_tables() -> None:
#    Base.metadata.create_all(bind=engine)
#
#
#def password_hash(password: str) -> str:
#    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
#
#
#def password_matches(password: str, hashed: str) -> bool:
#    return bcrypt.checkpw(password.encode(), hashed.encode())
#
#
#def create_token(user_id: int) -> str:
#    return jwt.encode({"sub": str(user_id)}, JWT_SECRET, algorithm="HS256")
#
#
#def user_response(user: User) -> UserResponse:
#    parts = user.name.strip().split()
#    return UserResponse(
#        id=user.id,
#        name=user.name,
#        email=user.email,
#        firstName=parts[0] if parts else "",
#        lastName=" ".join(parts[1:]),
#        initials="".join(part[0] for part in parts[:2]).upper() or "ET",
#        institution=user.institution,
#        level=user.level,
#        admin=user.admin,
#    )
#
#
#def current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> User:
#    if not authorization or not authorization.startswith("Bearer "):
#        raise HTTPException(status_code=401, detail="Non authentifié")
#    try:
#        payload = jwt.decode(authorization.removeprefix("Bearer ").strip(), JWT_SECRET, algorithms=["HS256"])
#        user_id = int(payload["sub"])
#    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
#        raise HTTPException(status_code=401, detail="Session invalide") from None
#    user = db.get(User, user_id)
#    if user is None:
#        raise HTTPException(status_code=401, detail="Utilisateur introuvable")
#    return user
#
#
#@app.get("/")
#def root() -> dict[str, str]:
#    return {"message": "Annalis API is running"}
#
#
#@app.get("/health")
#def health() -> dict[str, str]:
#    return {"status": "ok"}
#
#
#@app.post("/auth/register", response_model=AuthResponse, status_code=201)
#def register(payload: RegisterPayload, db: Session = Depends(get_db)):
#    email = str(payload.email).lower()
#    if db.scalar(select(User).where(User.email == email)):
#        return JSONResponse(status_code=409, content={"message": "Cette adresse e-mail est déjà utilisée"})
#    user = User(name=payload.name.strip(), email=email, password_hash=password_hash(payload.password))
#    db.add(user)
#    db.commit()
#    db.refresh(user)
#    return {"token": create_token(user.id), "user": user_response(user)}
#
#
#@app.post("/auth/login", response_model=AuthResponse)
#def login(payload: Credentials, db: Session = Depends(get_db)):
#    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
#    if user is None or not password_matches(payload.password, user.password_hash):
#        return JSONResponse(status_code=401, content={"message": "E-mail ou mot de passe incorrect"})
#    return {"token": create_token(user.id), "user": user_response(user)}
#
#
#@app.get("/auth/me", response_model=UserResponse)
#def me(user: User = Depends(current_user)):
#    return user_response(user)
#
#
#@app.post("/auth/logout")
#def logout(_: User = Depends(current_user)):
#    return {"message": "Déconnexion réussie"}
#
#
#def format_size(size: int) -> str:
#    if size < 1024 * 1024:
#        return f"{round(size / 1024)} Ko"
#    return f"{size / (1024 * 1024):.1f}".replace(".", ",") + " Mo"
#
#
#def document_response(document: Document) -> dict:
#    author = document.owner.name
#    return {
#        "id": document.id,
#        "title": document.title,
#        "subject": document.subject,
#        "format": document.format,
#        "size": format_size(document.size_bytes),
#        "author": author,
#        "initials": "".join(part[0] for part in author.split()[:2]).upper() or "ET",
#        "date": document.created_at.strftime("%d %b %Y"),
#        "tone": {"PDF": "blue", "DOCX": "purple", "PPTX": "coral"}.get(document.format, "green"),
#        "downloads": document.downloads,
#        "verified": document.verified,
#    }
#
#
#@app.get("/documents")
#def list_documents(
#    q: str | None = Query(default=None),
#    subject: str | None = Query(default=None),
#    format: str | None = Query(default=None),
#    page: int = Query(default=1, ge=1),
#    db: Session = Depends(get_db),
#    _: User = Depends(current_user),
#):
#    query = select(Document).join(Document.owner).options(joinedload(Document.owner)).where(Document.verified.is_(True))
#    if q:
#        term = f"%{q.strip()}%"
#        query = query.where(or_(Document.title.ilike(term), Document.subject.ilike(term), User.name.ilike(term)))
#    if subject:
#        query = query.where(Document.subject == subject)
#    if format:
#        query = query.where(Document.format == format.upper())
#    total_query = select(func.count()).select_from(query.subquery())
#    total = db.scalar(total_query) or 0
#    documents = db.scalars(query.order_by(Document.created_at.desc()).offset((page - 1) * 50).limit(50)).unique().all()
#    return {"data": [document_response(document) for document in documents], "total": total}
#
#
#def validate_upload(upload: UploadFile) -> tuple[str, str]:
#    extension = Path(upload.filename or "").suffix.lower()
#    if extension not in ALLOWED_EXTENSIONS:
#        raise HTTPException(status_code=422, detail="Format accepté : PDF, DOCX ou PPTX")
#    return extension, ALLOWED_EXTENSIONS[extension]
#
#
#@app.post("/documents", status_code=201)
#async def upload_document(
#    file: UploadFile = File(...),
#    title: str = Form(...),
#    subject: str = Form(...),
#    level: str = Form("Licence 1"),
#    description: str | None = Form(None),
#    user: User = Depends(current_user),
#    db: Session = Depends(get_db),
#):
#    extension, format_name = validate_upload(file)
#    content = await file.read()
#    if not content:
#        raise HTTPException(status_code=422, detail="Le fichier est vide")
#    if len(content) > MAX_FILE_SIZE:
#        raise HTTPException(status_code=413, detail="Le fichier ne doit pas dépasser 20 Mo")
#    stored_filename = f"{secrets.token_urlsafe(24)}{extension}"
#    (UPLOAD_DIR / stored_filename).write_bytes(content)
#    document = Document(
#        title=title.strip(), subject=subject.strip(), level=level.strip(),
#        description=description.strip() if description else None,
#        original_filename=file.filename or stored_filename, stored_filename=stored_filename,
#        format=format_name, size_bytes=len(content), owner_id=user.id,
#    )
#    db.add(document)
#    db.commit()
#    db.refresh(document)
#    document.owner = user
#    return document_response(document)
#
#
#def find_document(document_id: int, db: Session) -> Document:
#    document = db.scalar(select(Document).options(joinedload(Document.owner)).where(Document.id == document_id))
#    if document is None:
#        raise HTTPException(status_code=404, detail="Document introuvable")
#    return document
#
#
#@app.get("/documents/{document_id}/download")
#def download_document(document_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
#    document = find_document(document_id, db)
#    path = UPLOAD_DIR / document.stored_filename
#    if not path.is_file():
#        raise HTTPException(status_code=404, detail="Fichier introuvable")
#    document.downloads += 1
#    db.commit()
#    return FileResponse(path, filename=document.original_filename, media_type=mimetypes.guess_type(path.name)[0])
#
#
#@app.get("/documents/{document_id}/file")
#def file_alias(document_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
#    return download_document(document_id, db, user)
#
#
#@app.get("/documents/{document_id}/view")
#def view_document(document_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
#    document = find_document(document_id, db)
#    path = UPLOAD_DIR / document.stored_filename
#    if not path.is_file():
#        raise HTTPException(status_code=404, detail="Fichier introuvable")
#    response = FileResponse(path, media_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream")
#    response.headers["Content-Disposition"] = f'inline; filename="{quote(document.original_filename)}"'
#    return response
#