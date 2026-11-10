from src.main.api.models.base_model import BaseModel


class CreateDepositRequest(BaseModel):
    accountId: int
    amount: float

