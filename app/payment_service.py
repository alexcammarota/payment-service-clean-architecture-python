import uuid
from datetime import datetime, UTC
from uuid import UUID

from app.payment_models import Payment, PaymentRequest, PaymentStatus, PaymentMethod
from app.payment_notification_service import PaymentNotificationService
from app.payment_processor import PaymentProcessor
from app.payment_repository import PaymentRepository
from app.payment_validator import PaymentValidator


class PaymentService:
    def __init__(self, payment_validator: PaymentValidator,
                 payment_repository: PaymentRepository,
                 payment_notification_service: PaymentNotificationService,
                 payment_processors: list[PaymentProcessor]) -> None:
        self._payment_validator = payment_validator
        self._payment_repository = payment_repository
        self._payment_notification_service = payment_notification_service
        self._payment_processors = payment_processors

    def process(self, request: PaymentRequest) -> Payment:
        self._payment_validator.validate(request)

        payment = Payment(
            paymentId=uuid.uuid4(),
            customerId=request.customer_id,
            amount=request.amount,
            currency=request.currency,
            paymentMethod=request.payment_method,
            status=PaymentStatus.PENDING,
            createdAt=datetime.now(UTC)
        )

        processor = next((processor for processor in self._payment_processors
                          if processor.supports(payment.payment_method)), None)

        if processor is None:
            raise ValueError(f"Unsupported Payment Method {payment.payment_method}")

        processor.process(payment)

        self._payment_repository.save(payment)

        self._payment_notification_service.send(payment)

        return payment

    def find_by_id(self, payment_id: UUID) -> Payment:
        payment = self._payment_repository.find_by_id(payment_id)

        if payment is None:
            raise KeyError(f"Payment not Found {payment_id}")

        return payment
