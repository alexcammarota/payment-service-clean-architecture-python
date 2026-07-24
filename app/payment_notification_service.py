from typing import Protocol

from app.payment_models import Payment


class PaymentNotifier(Protocol):

    def send(self, payment: Payment) -> None:
        ...


class PaymentNotificationService(PaymentNotifier):

    def send(self, payment: Payment) -> None:
        print(
            f"Payment notification sent: "
            f"id={payment.payment_id}, "
            f"status={payment.status}"
        )
