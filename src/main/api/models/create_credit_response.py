from src.main.api.models.base_model import BaseModel


class CreateCreditResponse(BaseModel):
    id: int
    amount: int
    balance: int
    creditId: int