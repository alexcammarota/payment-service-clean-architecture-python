from uuid import UUID

from fastapi import FastAPI, HTTPException
from starlette import status

from app.application.boundaries.payment_boundaries import ProcessPayment, GetPayment
from app.application.usecase.GetPaymentUseCase import GetPaymentUseCase
from app.application.usecase.ProcessPaymentUseCase import ProcessPaymentUseCase
from app.presentation.rest.payment_models import PaymentRequest, PaymentResponse
from app.infrastructure.notification.console_payment_notifier import ConsolePaymentNotifier
from app.infrastructure.processors.payment_processors import PixPaymentProcessor, CreditCardPaymentProcessor, \
    BankTransferPaymentProcessor
from app.infrastructure.persistence.in_memory_payment_repository import InMemoryPaymentRepository
from app.application.validation.payment_validator import PaymentValidator

app = FastAPI(title="Payment Service",
              version="0.1.0")

payment_repository = InMemoryPaymentRepository()
payment_notifier = ConsolePaymentNotifier()
payment_processors = [PixPaymentProcessor(), CreditCardPaymentProcessor(), BankTransferPaymentProcessor()]

process_payment_usecase: ProcessPayment = ProcessPaymentUseCase(payment_validator=PaymentValidator(),
                                                        payment_repository=payment_repository,
                                                        payment_notifier=payment_notifier,
                                                        payment_processors=payment_processors)


get_payment_usecase: GetPayment = GetPaymentUseCase(payment_repository=payment_repository)


@app.get("/healthcheck")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/payments",
          response_model=PaymentResponse,
          status_code=status.HTTP_201_CREATED)
def process_payment(request: PaymentRequest) -> PaymentResponse:
    try:
        payment = process_payment_usecase.process(request.to_command())
        return PaymentResponse.from_payment(payment)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@app.get("/api/v1/payments/{payment_id}",
         response_model=PaymentResponse,
         status_code=status.HTTP_200_OK)
def find_by_id_payment(payment_id: UUID) -> PaymentResponse:
    try:
        payment = get_payment_usecase.find_by_id(payment_id)
        return PaymentResponse.from_payment(payment)
    except KeyError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
