from src.main.api.models.base_model import BaseModel


class CreateDepositResponse(BaseModel):
    id: int
    balance: float
