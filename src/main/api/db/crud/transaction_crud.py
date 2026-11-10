from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_transactions_by_account_id(db: Session, account_id: int):
        outgoing = db.query(Transaction).filter_by(from_account_id=account_id).all()
        incoming = db.query(Transaction).filter_by(to_account_id=account_id).all()

        return outgoing + incoming