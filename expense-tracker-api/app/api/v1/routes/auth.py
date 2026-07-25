from fastapi import APIRouter, HTTPException, status

from app.api.deps import DbDep
from app.core.exceptions import AlreadyExistsError, InvalidCredentialsError
from app.schemas.user import LoginRequest, Token, UserCreate, UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: DbDep):
    service = AuthService(db)
    try:
        user = service.register(payload.email, payload.password)
    except AlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return user


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: DbDep):
    service = AuthService(db)
    try:
        token = service.authenticate(payload.email, payload.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    return Token(access_token=token)
