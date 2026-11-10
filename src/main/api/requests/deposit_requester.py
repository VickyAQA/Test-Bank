from http import HTTPStatus

from src.main.api.models.deposit_request import CreateDepositRequest
from src.main.api.models.deposit_response import CreateDepositResponse
from src.main.api.requests.requester import Requester
import requests


class DepositRequester(Requester):
    def post(self, create_credit_request: CreateDepositRequest):
        url = f"{self.base_url}/account/deposit"
        response = requests.post(
            url=url,
            json=create_credit_request.model_dump(),
            headers=self.headers
        )

        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return CreateDepositResponse(**response.json())
        return response


