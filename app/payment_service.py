import uuid
from datetime import datetime, UTC
from decimal import Decimal
from uuid import UUID

from app.payment_models import Payment, PaymentRequest, PaymentStatus, PaymentMethod


class PaymentService:
    def __init__(self) -> None:
        self._payments: dict[UUID, Payment] = {}

    def process(self, request: PaymentRequest) -> Payment:
        self._validate(request)

        payment = Payment(
            paymentId=uuid.uuid4(),
            customerId=request.customer_id,
            amount=request.amount,
            currency=request.currency,
            paymentMethod=request.payment_method,
            status=PaymentStatus.PENDING,
            createdAt=datetime.now(UTC)
        )

        if request.payment_method == PaymentMethod.PIX:
            payment.status = PaymentStatus.APPROVED
        elif request.payment_method == PaymentMethod.CREDIT_CARD:
            payment.status = PaymentStatus.APPROVED
        elif request.payment_method == PaymentMethod.BANK_TRANSFER:
            payment.status = PaymentStatus.PENDING
        else:
            payment.status = PaymentStatus.REJECTED

        self._payments[payment.payment_id] = payment

        print(
            f"Payment notification sent: "
            f"id={payment.payment_id}, "
            f"status={payment.status}"
        )

        return payment

    def find_by_id(self, payment_id: UUID) -> Payment:
        payment = self._payments.get(payment_id)

        if payment is None:
            raise KeyError(f"Payment not Found {payment_id}")

        return payment

    @staticmethod
    def _validate(request: PaymentRequest) -> None:
        if request.amount <= Decimal("0"):
            raise ValueError("Payment amount must be greater than zero")

        if not request.currency.strip():
            raise ValueError("Currency must be informed")


