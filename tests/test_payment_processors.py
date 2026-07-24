from datetime import datetime, UTC
from decimal import Decimal
from uuid import uuid4

import pytest

from app.domain.payment import PaymentMethod, PaymentStatus, Payment
from app.infrastructure.processors.payment_processors import PixPaymentProcessor, CreditCardPaymentProcessor, \
    BankTransferPaymentProcessor


def create_payment(payment_method: PaymentMethod) -> Payment:
    return Payment(
        payment_id=uuid4(),
        customer_id=uuid4(),
        amount=Decimal("100.00"),
        currency="BRL",
        payment_method=payment_method,
        status=PaymentStatus.PENDING,
        created_at=datetime.now(UTC),
    )


@pytest.mark.parametrize(
    ("processor", "payment_method", "expected_status"),
    [
        (
            PixPaymentProcessor(),
            PaymentMethod.PIX,
            PaymentStatus.APPROVED,
        ),
        (
            CreditCardPaymentProcessor(),
            PaymentMethod.CREDIT_CARD,
            PaymentStatus.APPROVED,
        ),
        (
            BankTransferPaymentProcessor(),
            PaymentMethod.BANK_TRANSFER,
            PaymentStatus.PENDING,
        ),
    ],
)
def test_processor_respects_contract(
    processor,
    payment_method,
    expected_status,
) -> None:
    payment = create_payment(payment_method)

    payment_id = payment.payment_id
    customer_id = payment.customer_id
    amount = payment.amount
    currency = payment.currency

    assert processor.supports(payment_method)

    processor.process(payment)

    assert payment.status == expected_status
    assert payment.payment_id == payment_id
    assert payment.customer_id == customer_id
    assert payment.amount == amount
    assert payment.currency == currency
