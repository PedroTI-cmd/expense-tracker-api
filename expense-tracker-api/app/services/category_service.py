import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.repo = CategoryRepository(db)

    def list_categories(self, owner_id: uuid.UUID) -> list[Category]:
        return self.repo.list_by_owner(owner_id)

    def create_category(self, owner_id: uuid.UUID, name: str) -> Category:
        return self.repo.create(name=name, owner_id=owner_id)

    def _get_owned_or_raise(self, category_id: uuid.UUID, owner_id: uuid.UUID) -> Category:
        category = self.repo.get_by_id(category_id, owner_id)
        if category is None:
            raise NotFoundError("Categoria não encontrada.")
        return category

    def update_category(self, category_id: uuid.UUID, owner_id: uuid.UUID, name: str) -> Category:
        category = self._get_owned_or_raise(category_id, owner_id)
        return self.repo.update(category, name)

    def delete_category(self, category_id: uuid.UUID, owner_id: uuid.UUID) -> None:
        category = self._get_owned_or_raise(category_id, owner_id)
        # Gastos vinculados: a FK usa ondelete=SET NULL, então viram "sem categoria"
        self.repo.delete(category)
