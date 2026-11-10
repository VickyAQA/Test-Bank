from http import HTTPStatus

from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse
from src.main.api.requests.requester import Requester
import requests


class TransferRequester(Requester):
    def post(self, create_credit_request: TransferRequest):
        url = f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=create_credit_request.model_dump(),
            headers=self.headers
        )

        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return TransferResponse(**response.json())
        return response
