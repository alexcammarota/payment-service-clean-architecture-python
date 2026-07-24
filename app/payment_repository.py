from typing import Protocol
from uuid import UUID

from app.payment_models import Payment


class PaymentRepository(Protocol):

    def save(self, payment: Payment) -> Payment:
        ...

    def find_by_id(self, payment_id: UUID) -> Payment:
        ...


class InMemoryPaymentRepository(PaymentRepository):

    def __init__(self) -> None:
        self._payments: dict[UUID, Payment] = {}

    def save(self, payment: Payment) -> Payment:
        self._payments[payment.payment_id] = payment
        return payment

    def find_by_id(self, payment_id: UUID) -> Payment:
        return self._payments.get(payment_id)
