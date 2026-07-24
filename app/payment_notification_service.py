from app.payment_models import Payment


class PaymentNotificationService:
    @staticmethod
    def send(payment: Payment) -> None:
        print(
            f"Payment notification sent: "
            f"id={payment.payment_id}, "
            f"status={payment.status}"
        )
