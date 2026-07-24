from abc import abstractmethod
from typing import Protocol

from app.domain.payment import Payment


class PaymentNotifier(Protocol):
    @abstractmethod
    def send(self, payment: Payment) -> None:
        ...
