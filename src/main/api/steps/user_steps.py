import allure
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import CreateDepositRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest


class UserSteps(BaseSteps):
    @staticmethod
    def create_account(create_user_request: CreateUserRequest):
        with allure.step(f"Создание счета для пользователя {create_user_request.username}"):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_ACCOUNT,
                ResponseSpecs.request_created()
            ).post()
            return response

    @staticmethod
    def deposit(create_user_request: CreateUserRequest, deposit_request: CreateDepositRequest):
        with allure.step(f"Пополнение счета {deposit_request.accountId} на сумму {deposit_request.amount}"):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.DEPOSIT,
                ResponseSpecs.request_ok()
            ).post(deposit_request)
            return response

    @staticmethod
    def deposit_invalid(create_user_request: CreateUserRequest, deposit_request: CreateDepositRequest):
        with allure.step(f"Невалидное пополнение счета {deposit_request.accountId}"):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.DEPOSIT,
                ResponseSpecs.request_bad()
            ).post(deposit_request)
            return response

    @staticmethod
    def transfer(create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        with allure.step(
                f"Перевод {transfer_request.amount} со счета {transfer_request.fromAccountId} "
                f"на {transfer_request.toAccountId}"
        ):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.TRANSFER,
                ResponseSpecs.request_ok()
            ).post(transfer_request)
            return response

    @staticmethod
    def transfer_invalid(create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        with allure.step(f"Перевод на несуществующий счет {transfer_request.toAccountId}"):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.TRANSFER,
                ResponseSpecs.request_not_found()
            ).post(transfer_request)
            return response

    @staticmethod
    def transfer_invalid_amount(create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        with allure.step(f"Перевод с невалидной суммой {transfer_request.amount}"):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.TRANSFER,
                ResponseSpecs.request_bad()
            ).post(transfer_request)
            return response

    @staticmethod
    def get_account_transactions(create_user_request: CreateUserRequest, account_id: int):
        with allure.step(f"Получение истории транзакций счета {account_id}"):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.GET_HISTORY,
                ResponseSpecs.request_ok()
            ).get(account_id)
            return response

    @staticmethod
    def get_account_transactions_invalid(create_user_request: CreateUserRequest, account_id: int):
        with allure.step(f"Запрос истории несуществующего счета {account_id}"):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.GET_HISTORY,
                ResponseSpecs.request_not_found()
            ).get(account_id)
            return response

    @staticmethod
    def create_account_unauthorized():
        with allure.step("Попытка создания счета без авторизации"):
            response = CrudRequester(
                RequestSpecs.unauth_headers(),
                Endpoint.CREATE_ACCOUNT,
                ResponseSpecs.request_unauthorized()
            ).post()
            return response

    @staticmethod
    def create_credit(create_user_request: CreateUserRequest, credit_request: CreateCreditRequest):
        with allure.step(f"Запрос кредита на сумму {credit_request.amount} на срок {credit_request.termMonths} мес."):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_CREDIT,
                ResponseSpecs.request_created()
            ).post(credit_request)
            return response

    @staticmethod
    def create_credit_invalid(create_user_request: CreateUserRequest, credit_request: CreateCreditRequest):
        with allure.step(f"Запрос кредита с невалидной суммой {credit_request.amount}"):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_CREDIT,
                ResponseSpecs.request_bad()
            ).post(credit_request)
            return response

    @staticmethod
    def repay_credit(create_user_request: CreateUserRequest, repay_request: RepayCreditRequest):
        with allure.step(f"Погашение кредита {repay_request.creditId} на сумму {repay_request.amount}"):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.REPAY_CREDIT,
                ResponseSpecs.request_ok()
            ).post(repay_request)
            return response

    @staticmethod
    def repay_credit_invalid(create_user_request: CreateUserRequest, repay_request: RepayCreditRequest):
        with allure.step(f"Попытка погашения несуществующего кредита {repay_request.creditId}"):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.REPAY_CREDIT,
                ResponseSpecs.request_not_found()
            ).post(repay_request)
            return response

    @staticmethod
    def get_account_transactions_forbidden(create_user_request: CreateUserRequest, account_id: int):
        with allure.step(f"Попытка получить историю чужого счета {account_id}"):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.GET_HISTORY,
                ResponseSpecs.request_not_found()
            ).get(account_id)
            return response