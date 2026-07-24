from uuid import UUID

from app.application.gateways.payment_repository import PaymentRepository
from app.domain.payment import Payment


class InMemoryPaymentRepository(PaymentRepository):

    def __init__(self) -> None:
        self._payments: dict[UUID, Payment] = {}

    def save(self, payment: Payment) -> Payment:
        self._payments[payment.payment_id] = payment
        return payment

    def find_by_id(self, payment_id: UUID) -> Payment:
        return self._payments.get(payment_id)
