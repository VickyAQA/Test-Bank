import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCredit:
    def test_create_credit_success(
            self,
            api_manager: ApiManager,
            credit_user: CreateUserRequest,
            credit_account: CreateAccountResponse,
            db_session: Session
    ):
        credit_amount = 5000
        credit_term = 11

        create_credit_request = CreateCreditRequest(
            accountId=credit_account.id, amount=credit_amount, termMonths=credit_term
        )
        response = api_manager.user_steps.create_credit(credit_user, create_credit_request)

        db_credit = CreditCrudDb.get_credit_by_id(db_session, response.creditId)

        assert db_credit is not None, "Кредит не найден в БД!"
        assert db_credit.amount == credit_amount, "Сумма кредита в БД не совпадает!"
        assert db_credit.term_months == credit_term, "Срок кредита в БД не совпадает!"

    @pytest.mark.parametrize("invalid_amount, term_months", [
        (4999, 11),
        (15001, 12),
        (20000, 6)
    ])
    def test_create_credit_limit_exceeded(
            self,
            api_manager: ApiManager,
            credit_user: CreateUserRequest,
            credit_account: CreateAccountResponse,
            invalid_amount: int,
            term_months: int,
            db_session: Session
    ):

        credit_request = CreateCreditRequest(
            accountId=credit_account.id, amount=invalid_amount, termMonths=term_months
        )
        response = api_manager.user_steps.create_credit_invalid(credit_user, credit_request)

        error_text = response.json().get("error", "")
        assert "Amount must be between" in error_text, f"Неожиданная ошибка: {error_text}"

        db_credits = CreditCrudDb.get_credits_by_account_id(db_session, credit_account.id)
        assert len(db_credits) == 0, "Ошибка: невалидный кредит записался в БД!"
