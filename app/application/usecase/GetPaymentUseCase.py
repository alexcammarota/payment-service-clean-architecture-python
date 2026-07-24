from uuid import UUID

from app.application.boundaries.payment_boundaries import GetPayment
from app.application.gateways.payment_repository import PaymentRepository
from app.domain.payment import Payment


class GetPaymentUseCase(GetPayment):

    def __init__(self, payment_repository: PaymentRepository):
        self._payment_repository = payment_repository

    def find_by_id(self, payment_id: UUID) -> Payment:
        payment = self._payment_repository.find_by_id(payment_id)

        if payment is None:
            raise KeyError(f"Payment not Found {payment_id}")

        return payment
