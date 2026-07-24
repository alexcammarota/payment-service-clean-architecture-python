from decimal import Decimal

from app.application.command.process_payment_command import ProcessPaymentCommand


class PaymentValidator:

    @staticmethod
    def validate(request: ProcessPaymentCommand) -> None:
        if request.amount <= Decimal("0"):
            raise ValueError("Payment amount must be greater than zero")

        if not request.currency.strip():
            raise ValueError("Currency must be informed")