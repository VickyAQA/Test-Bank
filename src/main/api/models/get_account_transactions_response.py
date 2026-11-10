from src.main.api.models.base_model import BaseModel
from typing import List, Optional

class TransactionsResponse(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: Optional[int] = None
    toAccountId: Optional[int] = None
    createdAt: str

class GetAccountTransactionsResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: List[TransactionsResponse]