import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.deposit_request import CreateDepositRequest
from src.main.api.models.create_credit_request import CreateCreditRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def created_account(api_manager, create_user_request):
    account = api_manager.user_steps.create_account(create_user_request)
    return account

@pytest.fixture
def funded_account(api_manager, create_user_request, created_account):
    deposit_amount = 1000
    deposit_request = CreateDepositRequest(accountId=created_account.id, amount=deposit_amount)
    api_manager.user_steps.deposit(create_user_request, deposit_request)
    return created_account, deposit_amount

@pytest.fixture
def created_credit(api_manager):
    user = RandomModelGenerator.generate(CreateUserRequest)
    user.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user)

    account = api_manager.user_steps.create_account(user)

    credit_request = CreateCreditRequest(accountId=account.id, amount=5000, termMonths=11)
    credit = api_manager.user_steps.create_credit(user, credit_request)

    return user, account, credit

@pytest.fixture
def credit_user(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def credit_account(api_manager, credit_user):
    return api_manager.user_steps.create_account(credit_user)


@pytest.fixture
def funded_credit(api_manager, created_credit):
    user, account, credit = created_credit

    deposit_amount = 2000
    deposit_request = CreateDepositRequest(accountId=account.id, amount=deposit_amount)
    api_manager.user_steps.deposit(user, deposit_request)
    return user, account, credit, deposit_amount