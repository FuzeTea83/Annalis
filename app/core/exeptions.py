class AppError(Exception):
    def __init__(self, message: str, code: str = "UNKNOWN"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class InvalidEmailDomainError(AppError):
    def __init__(self, allowed_domains: list[str]):
        message = f"L'email doit être un email valide de domaine {', '.join(allowed_domains)}"
        super().__init__(message, "INVALID_EMAIL_DOMAIN")

class InvalidCredentialsError(AppError):
    def __init__(self):
        super().__init__("Email ou mot de passe incorrect", "INVALID_CREDENTIALS")

class EmailAlreadyExistsError(AppError):
    def __init__(self):
        super().__init__("Cet email est déjà utilisé", "EMAIL_EXISTS")

class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(message, "CONFLICT")

class InvalidTokenError(AppError):
    def __init__(self):
        super().__init__("Token invalide ou expiré", "INVALID_TOKEN")

class UserNotFoundError(AppError):
    def __init__(self):
        super().__init__("Utilisateur non trouvé", "USER_NOT_FOUND")

class UnknownFileError(AppError):
    def __init__(self):
        super().__init__("Fichier non trouvé", "FILE_NOT_FOUND")

class InvalidFileTypeError(AppError):
    def __init__(self):
        super().__init__("Type de fichier non autorisé", "INVALID_FILE_TYPE")

class FileTooLargeError(AppError):
    def __init__(self, max_size_mb: int):
        super().__init__(f"Le fichier dépasse la taille maximale autorisée de {max_size_mb} Mo", "FILE_TOO_LARGE")

class DocumentNotFoundError(AppError):
    def __init__(self):
        super().__init__("Document non trouvé", "DOCUMENT_NOT_FOUND")