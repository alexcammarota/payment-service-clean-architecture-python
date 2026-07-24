import uuid
from datetime import datetime, UTC

from app.application.boundaries.payment_boundaries import ProcessPayment
from app.application.command.process_payment_command import ProcessPaymentCommand
from app.application.gateways.payment_notifier import PaymentNotifier
from app.application.gateways.payment_processor import PaymentProcessor
from app.application.gateways.payment_repository import PaymentRepository
from app.application.validation.payment_validator import PaymentValidator
from app.domain.payment import Payment, PaymentStatus


class ProcessPaymentUseCase(ProcessPayment):

    def __init__(self, payment_validator: PaymentValidator,
                 payment_repository: PaymentRepository,
                 payment_notifier: PaymentNotifier,
                 payment_processors: list[PaymentProcessor]) -> None:
        self._payment_validator = payment_validator
        self._payment_repository = payment_repository
        self.payment_notifier = payment_notifier
        self._payment_processors = payment_processors

    def process(self, command: ProcessPaymentCommand) -> Payment:
        self._payment_validator.validate(command)

        payment = Payment(
            payment_id=uuid.uuid4(),
            customer_id=command.customer_id,
            amount=command.amount,
            currency=command.currency,
            payment_method=command.payment_method,
            status=PaymentStatus.PENDING,
            created_at=datetime.now(UTC)
        )

        processor = next((processor for processor in self._payment_processors
                          if processor.supports(payment.payment_method)), None)

        if processor is None:
            raise ValueError(f"Unsupported Payment Method {payment.payment_method}")

        processor.process(payment)
        self._payment_repository.save(payment)
        self.payment_notifier.send(payment)

        return payment
