from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.payment import Payment


class PaymentRepository(Protocol):
    @abstractmethod
    def save(self, payment: Payment) -> Payment:
        ...

    @abstractmethod
    def find_by_id(self, payment_id: UUID) -> Payment:
        ...
