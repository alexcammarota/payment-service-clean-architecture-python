from uuid import UUID

from fastapi import FastAPI, HTTPException
from starlette import status

from app.payment_models import PaymentRequest, PaymentResponse
from app.payment_notification_service import PaymentNotificationService
from app.payment_processors import PixPaymentProcessor, CreditCardPaymentProcessor, BankTransferPaymentProcessor
from app.payment_repository import PaymentRepository
from app.payment_service import PaymentService
from app.payment_validator import PaymentValidator

app = FastAPI(title="Payment Service",
              version="0.1.0")

payment_service = PaymentService(payment_validator=PaymentValidator(),
                                 payment_repository=PaymentRepository(),
                                 payment_notification_service=PaymentNotificationService(),
                                 payment_processors=[PixPaymentProcessor(), CreditCardPaymentProcessor(),
                                                     BankTransferPaymentProcessor()])


@app.get("/healthcheck")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/payments",
          response_model=PaymentResponse,
          status_code=status.HTTP_201_CREATED)
def process_payment(request: PaymentRequest) -> PaymentResponse:
    try:
        payment = payment_service.process(request)
        return PaymentResponse.from_payment(payment)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@app.get("/api/v1/payments/{payment_id}",
         response_model=PaymentResponse,
         status_code=status.HTTP_200_OK)
def find_by_id_payment(payment_id: UUID) -> PaymentResponse:
    try:
        payment = payment_service.find_by_id(payment_id)
        return PaymentResponse.from_payment(payment)
    except KeyError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
