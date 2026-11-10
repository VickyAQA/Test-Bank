import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.generators.model_generator import RandomModelGenerator


@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit_success(self, api_manager: ApiManager, funded_credit, db_session: Session):
        user, account, credit, deposit_amount = funded_credit

        repay_request = RepayCreditRequest(creditId=credit.creditId, accountId=account.id, amount=credit.amount)
        api_manager.user_steps.repay_credit(user, repay_request)

        assert CreditCrudDb.get_credit_by_id(db_session, credit.creditId).balance == 0, "Кредит не обнулился!"
        assert AccountCrudDb.get_account_by_id(db_session, account.id).balance == deposit_amount, \
            "Баланс счета неверный!"

    def test_repay_credit_with_invalid_id(self, api_manager: ApiManager, created_credit, db_session: Session):
        user, account, credit = created_credit

        invalid_credit_id = RandomModelGenerator.generate_invalid_id()
        repay_amount = RandomModelGenerator.generate_transfer_amount()

        repay_request = RepayCreditRequest(creditId=invalid_credit_id, accountId=account.id, amount=repay_amount)

        response = api_manager.user_steps.repay_credit_invalid(user, repay_request)

        error_text = response.json().get("error", "")
        assert str(invalid_credit_id) in error_text, f"Неожиданная ошибка от сервера: {error_text}"

        db_credit = CreditCrudDb.get_credit_by_id(db_session, credit.creditId)
        assert db_credit.balance == -credit.amount, "Ошибка: баланс реального кредита изменился!"

