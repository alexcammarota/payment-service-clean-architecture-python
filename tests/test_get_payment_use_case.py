from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from app.application.gateways.payment_repository import PaymentRepository
from app.application.usecase.get_payment import GetPaymentUseCase
from app.domain.payment import Payment, PaymentMethod, PaymentStatus


def test_get_payment_use_case_returns_payment():
    # Arrange
    repository = create_autospec(PaymentRepository, instance=True)

    payment = Payment(
        payment_id=uuid4(),
        customer_id=uuid4(),
        amount=Decimal("100.00"),
        currency="BRL",
        payment_method=PaymentMethod.PIX,
        status=PaymentStatus.APPROVED,
        created_at=datetime.now(UTC),
    )

    repository.find_by_id.return_value = payment

    use_case = GetPaymentUseCase(
        payment_repository=repository,
    )

    # Act
    result = use_case.execute(payment.payment_id)

    # Assert
    assert result == payment

    repository.find_by_id.assert_called_once_with(
        payment.payment_id
    )


def test_get_payment_use_case_raises_error_when_payment_not_found():
    # Arrange
    repository = create_autospec(PaymentRepository, instance=True)

    repository.find_by_id.return_value = None

    use_case = GetPaymentUseCase(
        payment_repository=repository,
    )

    payment_id = uuid4()

    with pytest.raises(
        KeyError,
        match=f"Payment not found {payment_id}",
    ):
        use_case.execute(payment_id)

    repository.find_by_id.assert_called_once_with(payment_id)