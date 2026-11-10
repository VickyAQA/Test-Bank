import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(
            self,
            db_session: Session,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest
    ):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0, "Баланс нового счета в ответе API не равен 0!"

        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)

        assert account_from_db is not None, "Аккаунт не найден в БД!"
        assert account_from_db.id == response.id, "ID аккаунта в БД не совпадает с ответом API!"
        assert account_from_db.balance == 0, "Баланс счета в БД не равен 0!"

    def test_create_account_unauthorized(self, api_manager):
        api_manager.user_steps.create_account_unauthorized()


