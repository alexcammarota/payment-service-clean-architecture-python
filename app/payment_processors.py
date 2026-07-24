from typing import Protocol

from app.payment_models import PaymentMethod, Payment, PaymentStatus


class PaymentProcessor(Protocol):
    def supports(self, payment_method: PaymentMethod) -> bool:
        ...

    def process(self, payment: Payment) -> None:
        ...


class PixPaymentProcessor(PaymentProcessor):
    def supports(self, payment_method: PaymentMethod) -> bool:
        return payment_method == PaymentMethod.PIX

    def process(self, payment: Payment) -> None:
        payment.status = PaymentStatus.APPROVED


class CreditCardPaymentProcessor(PaymentProcessor):
    def supports(self, payment_method: PaymentMethod) -> bool:
        return payment_method == PaymentMethod.CREDIT_CARD

    def process(self, payment: Payment) -> None:
        payment.status = PaymentStatus.APPROVED


class BankTransferPaymentProcessor(PaymentProcessor):
    def supports(self, payment_method: PaymentMethod) -> bool:
        return payment_method == PaymentMethod.BANK_TRANSFER

    def process(self, payment: Payment) -> None:
        payment.status = PaymentStatus.PENDING
