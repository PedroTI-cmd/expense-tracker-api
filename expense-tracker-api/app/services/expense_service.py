import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.expense import Expense
from app.repositories.category_repository import CategoryRepository
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import MonthlySummary


class ExpenseService:
    def __init__(self, db: Session) -> None:
        self.repo = ExpenseRepository(db)
        self.category_repo = CategoryRepository(db)

    def list_expenses(
        self,
        owner_id: uuid.UUID,
        category_id: uuid.UUID | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None,
    ) -> list[Expense]:
        return self.repo.list_by_owner(owner_id, category_id, date_from, date_to, min_amount, max_amount)

    def _get_owned_or_raise(self, expense_id: uuid.UUID, owner_id: uuid.UUID) -> Expense:
        expense = self.repo.get_by_id(expense_id, owner_id)
        if expense is None:
            raise NotFoundError("Gasto não encontrado.")
        return expense

    def get_expense(self, expense_id: uuid.UUID, owner_id: uuid.UUID) -> Expense:
        return self._get_owned_or_raise(expense_id, owner_id)

    def create_expense(
        self,
        owner_id: uuid.UUID,
        description: str,
        amount: Decimal,
        expense_date: date,
        category_id: uuid.UUID | None,
    ) -> Expense:
        if category_id is not None:
            # Garante que a categoria pertence ao próprio usuário
            self._get_owned_category_or_raise(category_id, owner_id)
        return self.repo.create(
            owner_id=owner_id,
            description=description,
            amount=amount,
            expense_date=expense_date,
            category_id=category_id,
        )

    def _get_owned_category_or_raise(self, category_id: uuid.UUID, owner_id: uuid.UUID):
        category = self.category_repo.get_by_id(category_id, owner_id)
        if category is None:
            raise NotFoundError("Categoria não encontrada.")
        return category

    def update_expense(
        self,
        expense_id: uuid.UUID,
        owner_id: uuid.UUID,
        **fields,
    ) -> Expense:
        expense = self._get_owned_or_raise(expense_id, owner_id)
        category_id = fields.get("category_id")
        if category_id is not None:
            self._get_owned_category_or_raise(category_id, owner_id)
        return self.repo.update(expense, **fields)

    def delete_expense(self, expense_id: uuid.UUID, owner_id: uuid.UUID) -> None:
        expense = self._get_owned_or_raise(expense_id, owner_id)
        self.repo.delete(expense)

    def monthly_summary(self, owner_id: uuid.UUID, year: int, month: int) -> MonthlySummary:
        total, by_category = self.repo.monthly_summary(owner_id, year, month)
        return MonthlySummary(year=year, month=month, total=total, by_category=by_category)
