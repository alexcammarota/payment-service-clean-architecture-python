from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from app.domain.payment import PaymentMethod


@dataclass(frozen=True)
class ProcessPaymentCommand:
    customer_id: UUID
    amount: Decimal
    currency: str
    payment_method: PaymentMethod