from decimal import Decimal

from app.payment_models import PaymentRequest


class PaymentValidator:

    @staticmethod
    def validate(request: PaymentRequest) -> None:
        if request.amount <= Decimal("0"):
            raise ValueError("Payment amount must be greater than zero")

        if not request.currency.strip():
            raise ValueError("Currency must be informed")