from fastapi import APIRouter
from app.constants.categories import EXPENSE_CATEGORIES, INCOME_CATEGORIES

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/")
def get_categories():
    return {
        "expense": EXPENSE_CATEGORIES,
        "income": INCOME_CATEGORIES,
    }
