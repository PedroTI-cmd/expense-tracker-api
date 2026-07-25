import uuid

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUserDep, DbDep
from app.core.exceptions import NotFoundError
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("", response_model=list[CategoryRead])
def list_categories(current_user: CurrentUserDep, db: DbDep):
    return CategoryService(db).list_categories(current_user.id)


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, current_user: CurrentUserDep, db: DbDep):
    return CategoryService(db).create_category(current_user.id, payload.name)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: uuid.UUID, payload: CategoryUpdate, current_user: CurrentUserDep, db: DbDep):
    try:
        return CategoryService(db).update_category(category_id, current_user.id, payload.name)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: uuid.UUID, current_user: CurrentUserDep, db: DbDep):
    try:
        CategoryService(db).delete_category(category_id, current_user.id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
