import uuid
from datetime import date
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUserDep, DbDep
from app.core.exceptions import NotFoundError
from app.schemas.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate, MonthlySummary
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/gastos", tags=["gastos"])


@router.get("", response_model=list[ExpenseRead])
def list_expenses(
    current_user: CurrentUserDep,
    db: DbDep,
    category_id: uuid.UUID | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
):
    return ExpenseService(db).list_expenses(
        current_user.id, category_id, date_from, date_to, min_amount, max_amount
    )


@router.get("/resumo-mensal", response_model=MonthlySummary)
def monthly_summary(
    current_user: CurrentUserDep,
    db: DbDep,
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
):
    return ExpenseService(db).monthly_summary(current_user.id, year, month)


@router.get("/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_id: uuid.UUID, current_user: CurrentUserDep, db: DbDep):
    try:
        return ExpenseService(db).get_expense(expense_id, current_user.id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(payload: ExpenseCreate, current_user: CurrentUserDep, db: DbDep):
    try:
        return ExpenseService(db).create_expense(current_user.id, **payload.model_dump())
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{expense_id}", response_model=ExpenseRead)
def update_expense(expense_id: uuid.UUID, payload: ExpenseUpdate, current_user: CurrentUserDep, db: DbDep):
    try:
        return ExpenseService(db).update_expense(
            expense_id, current_user.id, **payload.model_dump(exclude_unset=True)
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: uuid.UUID, current_user: CurrentUserDep, db: DbDep):
    try:
        ExpenseService(db).delete_expense(expense_id, current_user.id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
