from datetime import datetime
from uuid import UUID

from _decimal import Decimal
from pydantic import BaseModel, Field

from app.application.command.process_payment_command import ProcessPaymentCommand
from app.domain.payment import PaymentMethod, PaymentStatus, Payment


class PaymentRequest(BaseModel):
    customer_id: UUID = Field(alias="customerId")
    amount: Decimal
    currency: str
    payment_method: PaymentMethod = Field(alias="paymentMethod")

    def to_command(self) -> ProcessPaymentCommand:
        return ProcessPaymentCommand(
            customer_id=self.customer_id,
            amount=self.amount,
            currency=self.currency,
            payment_method=self.payment_method,
        )


class PaymentResponse(BaseModel):
    payment_id: UUID = Field(alias="paymentId")
    customer_id: UUID = Field(alias="customerId")
    amount: Decimal
    currency: str
    payment_method: PaymentMethod = Field(alias="paymentMethod")
    status: PaymentStatus
    created_at: datetime = Field(alias="createdAt")

    @classmethod
    def from_payment(cls, payment: Payment) -> "PaymentResponse":
        return cls(
            paymentId=payment.payment_id,
            customerId=payment.customer_id,
            amount=payment.amount,
            currency=payment.currency,
            paymentMethod=payment.payment_method,
            status=payment.status,
            createdAt=payment.created_at
        )
