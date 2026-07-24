from app.application.gateways.payment_processor import PaymentProcessor
from app.domain.payment import PaymentMethod, PaymentStatus, Payment


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
