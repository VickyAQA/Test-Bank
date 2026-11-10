import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import CreateDepositRequest


@pytest.mark.api
class TestAccountDeposit:
    def test_deposit_success(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            created_account: CreateAccountResponse,
            db_session: Session
    ):
        deposit_amount = 1000.5
        deposit_request = CreateDepositRequest(accountId=created_account.id, amount=deposit_amount)
        api_manager.user_steps.deposit(create_user_request, deposit_request)

        db_account = AccountCrudDb.get_account_by_id(db_session, created_account.id)
        assert db_account.balance == deposit_amount, "Баланс в БД не совпадает!"

        db_transactions = TransactionCrudDb.get_transactions_by_account_id(db_session, created_account.id)
        deposit_tx = next((t for t in db_transactions if t.transaction_type == "deposit"), None)

        assert deposit_tx is not None, "Транзакция не найдена в БД!"
        assert deposit_tx.amount == deposit_amount, "Сумма транзакции в БД не совпадает!"

    @pytest.mark.parametrize("invalid_amount", [999, 9001, 0, -500])
    def test_deposit_invalid_amount(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            created_account: CreateAccountResponse,
            invalid_amount: int,
            db_session: Session
    ):
        deposit_request = CreateDepositRequest(accountId=created_account.id, amount=invalid_amount)
        response = api_manager.user_steps.deposit_invalid(create_user_request, deposit_request)

        assert "Amount must be between" in response.json().get("error", "")

        db_account = AccountCrudDb.get_account_by_id(db_session, created_account.id)
        assert db_account.balance == created_account.balance, "Ошибка: баланс изменился после невалидного депозита!"

    def test_deposit_without_amount(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            created_account: CreateAccountResponse,
            db_session: Session
    ):
        deposit_request = CreateDepositRequest.model_construct(accountId=created_account.id)
        response = api_manager.user_steps.deposit_invalid(create_user_request, deposit_request)

        assert "Amount is required" in response.json().get("error", "")

        db_account = AccountCrudDb.get_account_by_id(db_session, created_account.id)
        assert db_account.balance == created_account.balance, "Ошибка: баланс изменился после депозита без amount!"

