import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.expense import Expense


class ExpenseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_owner(
        self,
        owner_id: uuid.UUID,
        category_id: uuid.UUID | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None,
    ) -> list[Expense]:
        query = self.db.query(Expense).filter(Expense.owner_id == owner_id)
        if category_id is not None:
            query = query.filter(Expense.category_id == category_id)
        if date_from is not None:
            query = query.filter(Expense.expense_date >= date_from)
        if date_to is not None:
            query = query.filter(Expense.expense_date <= date_to)
        if min_amount is not None:
            query = query.filter(Expense.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Expense.amount <= max_amount)
        return query.order_by(Expense.expense_date.desc()).all()

    def get_by_id(self, expense_id: uuid.UUID, owner_id: uuid.UUID) -> Expense | None:
        return (
            self.db.query(Expense)
            .filter(Expense.id == expense_id, Expense.owner_id == owner_id)
            .first()
        )

    def create(self, owner_id: uuid.UUID, **kwargs) -> Expense:
        expense = Expense(owner_id=owner_id, **kwargs)
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def update(self, expense: Expense, **kwargs) -> Expense:
        for key, value in kwargs.items():
            if value is not None:
                setattr(expense, key, value)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete(self, expense: Expense) -> None:
        self.db.delete(expense)
        self.db.commit()

    def monthly_summary(self, owner_id: uuid.UUID, year: int, month: int) -> tuple[Decimal, dict[str, Decimal]]:
        rows = (
            self.db.query(Category.name, func.coalesce(func.sum(Expense.amount), 0))
            .join(Category, Category.id == Expense.category_id, isouter=True)
            .filter(
                Expense.owner_id == owner_id,
                func.extract("year", Expense.expense_date) == year,
                func.extract("month", Expense.expense_date) == month,
            )
            .group_by(Category.name)
            .all()
        )
        by_category = {(name or "Sem categoria"): total for name, total in rows}
        total = sum(by_category.values()) if by_category else Decimal("0")
        return total, by_category
