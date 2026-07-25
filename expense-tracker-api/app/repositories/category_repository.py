import uuid

from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_owner(self, owner_id: uuid.UUID) -> list[Category]:
        return self.db.query(Category).filter(Category.owner_id == owner_id).order_by(Category.name).all()

    def get_by_id(self, category_id: uuid.UUID, owner_id: uuid.UUID) -> Category | None:
        return (
            self.db.query(Category)
            .filter(Category.id == category_id, Category.owner_id == owner_id)
            .first()
        )

    def create(self, name: str, owner_id: uuid.UUID) -> Category:
        category = Category(name=name, owner_id=owner_id)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: Category, name: str) -> Category:
        category.name = name
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()
