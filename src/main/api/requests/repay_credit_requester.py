from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.repay_credit_response import RepayCreditResponse
from src.main.api.requests.requester import Requester
import requests


class RepayCreditRequester(Requester):
    def post(self, repay_credit_request: RepayCreditRequest):
        url = f"{self.base_url}/credit/repay"
        response = requests.post(
            url=url,
            json=repay_credit_request.model_dump(),
            headers=self.headers
        )

        self.response_spec(response)

        if response.status_code == 200:
            return RepayCreditResponse(**response.json())
        return response
