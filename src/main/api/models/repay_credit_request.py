from src.main.api.models.base_model import BaseModel

class RepayCreditRequest(BaseModel):
    creditId: int
    accountId: int
    amount: float