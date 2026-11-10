from enum import Enum

from src.main.api.models.base_model import BaseModel
from typing import Optional, Type
from dataclasses import dataclass
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.deposit_request import CreateDepositRequest
from src.main.api.models.deposit_response import CreateDepositResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse
from src.main.api.models.get_account_transactions_response import GetAccountTransactionsResponse
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_credit_response import CreateCreditResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.repay_credit_response import RepayCreditResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model = CreateUserRequest,
        url = "/admin/create",
        response_model = CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model = None,
        url = "/admin/users",
        response_model = None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model = LoginUserRequest,
        url = "/auth/token/login",
        response_model = LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model = None,
        url = "/account/create",
        response_model = CreateAccountResponse
    )

    DEPOSIT = EndpointConfiguration(
        request_model = CreateDepositRequest,
        url = "/account/deposit",
        response_model = CreateDepositResponse
    )

    TRANSFER = EndpointConfiguration(
        request_model = TransferRequest,
        url = "/account/transfer",
        response_model = TransferResponse
    )

    GET_HISTORY = EndpointConfiguration(
        request_model = None,
        url = "/account/transactions",
        response_model = GetAccountTransactionsResponse
    )

    CREATE_CREDIT = EndpointConfiguration(
        request_model = CreateCreditRequest,
        url = "/credit/request",
        response_model = CreateCreditResponse
    )

    REPAY_CREDIT = EndpointConfiguration(
        request_model = RepayCreditRequest,
        url = "/credit/repay",
        response_model = RepayCreditResponse
    )