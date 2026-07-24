from abc import abstractmethod
from typing import Protocol

from app.domain.payment import PaymentMethod, Payment


class PaymentProcessor(Protocol):

    @abstractmethod
    def supports(self, payment_method: PaymentMethod) -> bool:
        ...

    @abstractmethod
    def process(self, payment: Payment) -> None:
        ...
