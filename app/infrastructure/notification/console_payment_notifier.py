from app.application.gateways.payment_notifier import PaymentNotifier
from app.domain.payment import Payment


class ConsolePaymentNotifier(PaymentNotifier):

    def send(self, payment: Payment) -> None:
        print(
            f"Payment notification sent: "
            f"id={payment.payment_id}, "
            f"status={payment.status}"
        )
