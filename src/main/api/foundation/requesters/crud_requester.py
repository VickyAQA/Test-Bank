from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
from requests import Response
import requests
import allure


class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel] = None) -> Response:
        body = model.model_dump() if model is not None else ""

        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url}"):
            allure.attach(str(body), "Request body", allure.attachment_type.JSON)

            response = requests.post(
                url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}",
                headers=self.request_spec,
                json=body
            )

            allure.attach(
                response.text,
                "Response body",
                allure.attachment_type.JSON
            )
            self.response_spec(response)
            return response

    def delete(self, user_id: int) -> Response:
        with allure.step(f"DELETE {Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}"):
            response = requests.delete(
                url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}",
                headers=self.request_spec
            )
            allure.attach(response.text, "Response body", allure.attachment_type.JSON)
            self.response_spec(response)
            return response

    def get(self, account_id: int) -> Response:
        with allure.step(f"GET {Config.fetch('backendUrl')}{self.endpoint.value.url}/{account_id}"):
            response = requests.get(
                url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}/{account_id}",
                headers=self.request_spec
            )
            allure.attach(response.text, "Response body", allure.attachment_type.JSON)
            self.response_spec(response)
            return response