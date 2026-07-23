from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class PaymentMethod(StrEnum):
    PIX = "PIX"
    CREDIT_CARD = "CREDIT_CARD"
    BANK_TRANSFER = "BANK_TRANSFER"


class PaymentStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class PaymentRequest(BaseModel):
    customer_id: UUID = Field(alias="customerId")
    amount: Decimal
    currency: str
    payment_method: PaymentMethod = Field(alias="paymentMethod")


class Payment(BaseModel):
    payment_id: UUID = Field(alias="paymentId")
    customer_id: UUID = Field(alias="customerId")
    amount: Decimal
    currency: str
    payment_method: PaymentMethod = Field(alias="paymentMethod")
    status: PaymentStatus
    created_at: datetime = Field(alias="createdAt")


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
