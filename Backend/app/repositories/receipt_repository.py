"""Receipt repository."""

from sqlalchemy.orm import Session

from app.models.receipt import Receipt
from app.repositories.base import BaseRepository


class ReceiptRepository(BaseRepository[Receipt]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Receipt)
