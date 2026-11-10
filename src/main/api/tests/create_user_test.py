import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(
            self,
            api_manager: ApiManager,
            db_session: Session,
            create_user_request: CreateUserRequest,
    ):
        user_from_db = UserCrudDb.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is not None, "Созданного пользователя нет в БД!"
        assert user_from_db.username == create_user_request.username, "Имя пользователя в БД не совпадает!"
        assert user_from_db.role == create_user_request.role, "Роль пользователя в БД не совпадает!"

    @pytest.mark.parametrize(
        "username, password",
        [
            ("aбв", "pAss_W0RD"),
            ("ab", "pAss_W0RD"),
            ("abv!", "pAss_W0RD"),
            ("Vicky1", "pAss_W0Rд"),
            ("Vicky2", "pAss_W0"),
            ("Vicky3", "pass_w0rd"),
            ("Vicky4", "PASS_W0RD"),
            ("Vicky5", "PASSW0RD"),
            ("Vicky6", "PASS_WRRD"),

        ]

    )
    def test_create_user_invalid(self, db_session: Session, api_manager: ApiManager, username: str, password: str):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid(create_user_request)

        user_from_db = UserCrudDb.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, "Ошибка: невалидный пользователь записался в БД!"



