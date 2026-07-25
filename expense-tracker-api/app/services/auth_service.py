from sqlalchemy.orm import Session

from app.core.exceptions import AlreadyExistsError, InvalidCredentialsError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repo = UserRepository(db)

    def register(self, email: str, password: str) -> User:
        if self.repo.get_by_email(email):
            raise AlreadyExistsError("Já existe um usuário cadastrado com esse email.")
        return self.repo.create(email=email, hashed_password=hash_password(password))

    def authenticate(self, email: str, password: str) -> str:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Email ou senha inválidos.")
        return create_access_token(subject=str(user.id))
