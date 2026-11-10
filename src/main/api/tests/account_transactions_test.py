from typing import Tuple

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest


@pytest.mark.api
class TestAccountTransactions:
    def test_get_account_transactions_success(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            funded_account: Tuple[CreateAccountResponse, float]
    ):
        account1, _ = funded_account

        transfer_amount = 500
        account2 = api_manager.user_steps.create_account(create_user_request)

        transfer_request = TransferRequest(fromAccountId=account1.id, toAccountId=account2.id, amount=transfer_amount)
        api_manager.user_steps.transfer(create_user_request, transfer_request)

        history = api_manager.user_steps.get_account_transactions(create_user_request, account2.id)
        assert history.balance == transfer_amount

    def test_get_transactions_nonexistent_account(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.user_steps.get_account_transactions_invalid(
            create_user_request,
            999999
        )

        error_text = response.json().get("error", "")
        assert "999999" in error_text, f"Неожиданная ошибка от сервера: {error_text}"

    def test_get_transactions_foreign_account(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        second_user = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(second_user)
        foreign_account = api_manager.user_steps.create_account(second_user)

        response = api_manager.user_steps.get_account_transactions_forbidden(
            create_user_request,
            foreign_account.id
        )

        error_text = response.json().get("error", "")
        assert "not found or does not belong to" in error_text