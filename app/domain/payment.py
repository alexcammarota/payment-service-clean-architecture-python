from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from _decimal import Decimal
from pydantic import BaseModel, Field


class PaymentMethod(StrEnum):
    PIX = "PIX"
    CREDIT_CARD = "CREDIT_CARD"
    BANK_TRANSFER = "BANK_TRANSFER"


class PaymentStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


@dataclass
class Payment:
    payment_id: UUID
    customer_id: UUID
    amount: Decimal
    currency: str
    payment_method: PaymentMethod
    status: PaymentStatus
    created_at: datetime
