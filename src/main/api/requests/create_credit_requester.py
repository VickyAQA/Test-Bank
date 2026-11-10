from http import HTTPStatus

from src.main.api.models.create_credit_response import CreateCreditResponse
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.requests.requester import Requester
import requests


class CreateCreditRequester(Requester):
    def post(self, create_credit_request: CreateCreditRequest):
        url = f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            json=create_credit_request.model_dump(),
            headers=self.headers
        )

        self.response_spec(response)

        if response.status_code == HTTPStatus.CREATED:
            return CreateCreditResponse(**response.json())
        return response

