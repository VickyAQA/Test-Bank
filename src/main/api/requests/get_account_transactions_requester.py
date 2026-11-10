from src.main.api.requests.requester import Requester
from src.main.api.models.get_account_transactions_response import GetAccountTransactionsResponse
import requests


class GetAccountTransactionsRequester(Requester):
    def get(self, account_id: int) -> GetAccountTransactionsResponse:
        url = f"{self.base_url}/account/transactions/{account_id}"
        response = requests.get(
            url=url,
            headers=self.headers
        )

        self.response_spec(response)
        return GetAccountTransactionsResponse(**response.json())

    def post(self, model=None):
        raise NotImplementedError("Заглушка. Метод post не поддерживается")
