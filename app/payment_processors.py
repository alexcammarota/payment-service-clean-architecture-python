from app.payment_models import PaymentMethod, Payment, PaymentStatus


class PixPaymentProcessor:
    def supports(self, payment_method: PaymentMethod) -> bool:
        return payment_method == PaymentMethod.PIX

    def process(self, payment: Payment) -> None:
        payment.status = PaymentStatus.APPROVED


class CreditCardPaymentProcessor:
    def supports(self, payment_method: PaymentMethod) -> bool:
        return payment_method == PaymentMethod.CREDIT_CARD

    def process(self, payment: Payment) -> None:
        payment.status = PaymentStatus.APPROVED


class BankTransferPaymentProcessor:
    def supports(self, payment_method: PaymentMethod) -> bool:
        return payment_method == PaymentMethod.BANK_TRANSFER

    def process(self, payment: Payment) -> None:
        payment.status = PaymentStatus.PENDING
