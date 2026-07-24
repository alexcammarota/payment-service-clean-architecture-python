from typing import Protocol

from app.payment_models import PaymentMethod, Payment


class PaymentProcessor(Protocol):
    def supports(self, payment_method: PaymentMethod) -> bool:
        ...

    def process(self, payment: Payment) -> None:
        ...
