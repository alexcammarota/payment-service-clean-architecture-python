from decimal import Decimal
from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from app.application.command.process_payment_command import ProcessPaymentCommand
from app.application.gateways.payment_notifier import PaymentNotifier
from app.application.gateways.payment_processor import PaymentProcessor
from app.application.gateways.payment_repository import PaymentRepository
from app.application.usecase.process_payment import ProcessPaymentUseCase
from app.application.validation.payment_validator import PaymentValidator
from app.domain.payment import PaymentMethod, PaymentStatus


def test_process_payment_use_case():
    repository = create_autospec(PaymentRepository, instance=True)
    notifier = create_autospec(PaymentNotifier, instance=True)
    processor = create_autospec(PaymentProcessor, instance=True)

    processor.supports.return_value = True

    def approve_payment(payment):
        payment.status = PaymentStatus.APPROVED

    processor.process.side_effect = approve_payment

    use_case = ProcessPaymentUseCase(
        payment_validator=PaymentValidator(),
        payment_repository=repository,
        payment_notifier=notifier,
        payment_processors=[processor]
    )

    command = ProcessPaymentCommand(
        customer_id=uuid4(),
        amount=Decimal("100.00"),
        currency="BRL",
        payment_method=PaymentMethod.PIX,
    )

    payment = use_case.execute(command)

    assert payment.customer_id == command.customer_id
    assert payment.amount == command.amount
    assert payment.currency == command.currency
    assert payment.payment_method == command.payment_method
    assert payment.status == PaymentStatus.APPROVED

    processor.supports.assert_called_once_with(command.payment_method)
    processor.process.assert_called_once_with(payment)
    repository.save.assert_called_once_with(payment)
    notifier.send.assert_called_once_with(payment)


def test_process_payment_raises_error_when_processor_not_found():
    repository = create_autospec(PaymentRepository, instance=True)
    notifier = create_autospec(PaymentNotifier, instance=True)
    processor = create_autospec(PaymentProcessor, instance=True)

    processor.supports.return_value = False

    use_case = ProcessPaymentUseCase(
        payment_validator=PaymentValidator(),
        payment_repository=repository,
        payment_notifier=notifier,
        payment_processors=[processor],
    )

    command = ProcessPaymentCommand(
        customer_id=uuid4(),
        amount=Decimal("100.00"),
        currency="BRL",
        payment_method=PaymentMethod.PIX,
    )

    with pytest.raises(ValueError):
        use_case.execute(command)

    processor.process.assert_not_called()
    repository.save.assert_not_called()
    notifier.send.assert_not_called()


def test_process_payment_raises_error_when_amount_is_invalid():
    repository = create_autospec(PaymentRepository, instance=True)
    notifier = create_autospec(PaymentNotifier, instance=True)
    processor = create_autospec(PaymentProcessor, instance=True)

    use_case = ProcessPaymentUseCase(
        payment_validator=PaymentValidator(),
        payment_repository=repository,
        payment_notifier=notifier,
        payment_processors=[processor],
    )

    command = ProcessPaymentCommand(
        customer_id=uuid4(),
        amount=Decimal("0"),
        currency="BRL",
        payment_method=PaymentMethod.PIX,
    )

    with pytest.raises(
            ValueError,
            match="Payment amount must be greater than zero",
    ):
        use_case.execute(command)

    processor.supports.assert_not_called()
    processor.process.assert_not_called()
    repository.save.assert_not_called()
    notifier.send.assert_not_called()
