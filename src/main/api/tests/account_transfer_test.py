from typing import Tuple

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest


@pytest.mark.api
class TestAccountTransfer:
    def test_transfer_success(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            funded_account: Tuple[CreateAccountResponse, float],
            db_session: Session
    ):
        account1, deposit_amount = funded_account
        account2 = api_manager.user_steps.create_account(create_user_request)

        transfer_amount = 500
        transfer_request = TransferRequest(fromAccountId=account1.id, toAccountId=account2.id, amount=transfer_amount)
        api_manager.user_steps.transfer(create_user_request, transfer_request)

        assert AccountCrudDb.get_account_by_id(db_session, account1.id).balance == deposit_amount - transfer_amount
        assert AccountCrudDb.get_account_by_id(db_session, account2.id).balance == transfer_amount

    def test_transfer_to_nonexistent_account(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            funded_account: Tuple[CreateAccountResponse, float],
            db_session: Session
    ):
        account1, deposit_amount = funded_account

        transfer_amount = 500
        transfer_request = TransferRequest(
            fromAccountId=account1.id,
            toAccountId=999999,
            amount=transfer_amount
        )

        response = api_manager.user_steps.transfer_invalid(create_user_request, transfer_request)

        error_text = response.json().get("error", "")
        assert "999999" in error_text, f"Неожиданная ошибка от сервера: {error_text}"

        db_account1 = AccountCrudDb.get_account_by_id(db_session, account1.id)
        assert db_account1.balance == deposit_amount, "Ошибка: деньги списались, хотя перевод не прошел!"

    @pytest.mark.parametrize("invalid_amount", [499, 10001, 0, -100])
    def test_transfer_invalid_amount(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            funded_account: Tuple[CreateAccountResponse, float],
            invalid_amount: int,
            db_session: Session
    ):
        account1, deposit_amount = funded_account

        account2 = api_manager.user_steps.create_account(create_user_request)

        transfer_request = TransferRequest(fromAccountId=account1.id, toAccountId=account2.id, amount=invalid_amount)

        response = api_manager.user_steps.transfer_invalid_amount(create_user_request, transfer_request)

        error_text = response.json().get("error", "")
        assert "Amount must be between" in error_text, f"Неожиданная ошибка от сервера: {error_text}"

        db_account1 = AccountCrudDb.get_account_by_id(db_session, account1.id)
        db_account2 = AccountCrudDb.get_account_by_id(db_session, account2.id)

        assert db_account1.balance == deposit_amount, "Ошибка: баланс отправителя изменился!"
        assert db_account2.balance == 0, "Ошибка: баланс получателя изменился!"