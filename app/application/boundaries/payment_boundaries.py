from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.application.command.process_payment_command import ProcessPaymentCommand
from app.domain.payment import Payment


class ProcessPayment(Protocol):
    @abstractmethod
    def process(self, command: ProcessPaymentCommand) -> Payment:
        ...


class GetPayment(Protocol):
    @abstractmethod
    def find_by_id(self, payment_id: UUID) -> Payment:
        ...
