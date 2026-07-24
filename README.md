# Payment Service — SOLID & Clean Architecture with Python

A small payment processing API built with **Python** and **FastAPI** to demonstrate the practical application of **SOLID principles**, **Dependency Inversion**, and **Clean Architecture**.

The project intentionally focuses on architecture and code organization rather than production infrastructure.

## Goals

This project was created to demonstrate:

* SOLID principles applied in Python
* Separation of concerns
* Dependency Inversion using `Protocol`
* Explicit application boundaries and gateways
* Use cases isolated from HTTP and infrastructure concerns
* Framework-independent domain models
* Dependency injection through a composition root
* Unit testing of use cases with mocks

## Tech Stack

* Python
* FastAPI
* Pydantic
* pytest
* `unittest.mock`
* uv
* Ruff

## Architecture

The project follows a Clean Architecture-inspired structure:

```text
app/
├── domain/
│   └── payment.py
│
├── application/
│   ├── commands/
│   │   └── process_payment_command.py
│   │
│   ├── boundaries/
│   │   └── payment_boundaries.py
│   │
│   ├── gateways/
│   │   ├── payment_repository.py
│   │   ├── payment_notifier.py
│   │   └── payment_processor.py
│   │
│   ├── usecases/
│   │   ├── process_payment.py
│   │   └── get_payment.py
│   │
│   └── validation/
│       └── payment_validator.py
│
├── infrastructure/
│   ├── notification/
│   │   └── console_payment_notifier.py
│   │
│   ├── persistence/
│   │   └── in_memory_payment_repository.py
│   │
│   └── processors/
│       └── payment_processors.py
│
├── presentation/
│   └── rest/
│       └── payment_models.py
│
└── main.py

tests/
├── test_payment_processors.py
├── test_process_payment_use_case.py
└── test_get_payment_use_case.py
```

## Dependency Rule

Dependencies point toward the inner layers.

```text
Presentation
     ↓
Application
     ↓
Domain

Infrastructure
     ↓
Application Gateways
```

The application layer does not depend on FastAPI or concrete infrastructure implementations.

For example:

```text
HTTP Request
    ↓
PaymentRequest
    ↓
ProcessPaymentCommand
    ↓
ProcessPayment
    ↓
ProcessPaymentUseCase
    ↓
PaymentProcessor / PaymentRepository / PaymentNotifier
    ↑
Infrastructure implementations
```

## Request, Command and Domain Model

The project deliberately separates external API models from application and domain objects.

### PaymentRequest

Belongs to the presentation layer and represents the HTTP request.

```text
JSON
 ↓
PaymentRequest
```

### ProcessPaymentCommand

Belongs to the application layer and represents the intention to process a payment.

```text
PaymentRequest
      ↓
ProcessPaymentCommand
```

This prevents the application layer from depending on FastAPI or Pydantic request models.

### Payment

Belongs to the domain layer and represents a payment inside the system.

The domain model is implemented as a plain Python dataclass and does not depend on Pydantic or FastAPI.

```text
PaymentRequest
      ↓
ProcessPaymentCommand
      ↓
ProcessPaymentUseCase
      ↓
Payment
```

## Application Boundaries

Input boundaries define what operations the application exposes.

Examples:

```python
class ProcessPayment(Protocol):
    @abstractmethod
    def execute(
        self,
        command: ProcessPaymentCommand,
    ) -> Payment:
        ...
```

```python
class GetPayment(Protocol):
    @abstractmethod
    def execute(
        self,
        payment_id: UUID,
    ) -> Payment:
        ...
```

Their implementations are:

```text
ProcessPayment
      ↑
ProcessPaymentUseCase
```

and:

```text
GetPayment
      ↑
GetPaymentUseCase
```

This allows the presentation layer to depend on application contracts rather than concrete implementations.

## Application Gateways

The application defines contracts for operations that depend on external implementations.

Examples:

```text
PaymentRepository
PaymentNotifier
PaymentProcessor
```

Concrete implementations live outside the application layer:

```text
PaymentRepository
       ↑
InMemoryPaymentRepository
```

```text
PaymentNotifier
       ↑
ConsolePaymentNotifier
```

```text
PaymentProcessor
       ↑
PixPaymentProcessor
CreditCardPaymentProcessor
BankTransferPaymentProcessor
```

Python `Protocol` is used to define these contracts.

Explicit inheritance is used in this project to make the relationship between contracts and implementations clear.

## SOLID Principles

### Single Responsibility Principle — SRP

Responsibilities that initially belonged to a single payment service were separated.

Examples:

```text
PaymentValidator
→ validates payment input

PaymentProcessor
→ processes a payment method

PaymentRepository
→ persists payments

PaymentNotifier
→ sends notifications

ProcessPaymentUseCase
→ orchestrates the payment processing flow
```

Each component has a focused reason to change.

### Open/Closed Principle — OCP

Payment processing does not depend on an `if/elif` chain for every payment method.

Instead, processors implement the `PaymentProcessor` contract.

```text
PaymentProcessor
      ↑
PixPaymentProcessor
CreditCardPaymentProcessor
BankTransferPaymentProcessor
```

Adding a new payment method can be done by creating another processor without changing the `ProcessPaymentUseCase`.

Example:

```text
PayPalPaymentProcessor
```

can be added and injected into the processor list.

### Liskov Substitution Principle — LSP

All payment processors follow the same behavioral contract and can be used by the application without special treatment.

Contract tests verify that processors:

* support their expected payment method
* process a payment using the same contract
* produce a valid payment state

The use case works with `PaymentProcessor` instead of knowing which concrete processor it receives.

### Interface Segregation Principle — ISP

Contracts are intentionally small and focused.

For example:

```python
class PaymentNotifier(Protocol):
    def send(self, payment: Payment) -> None:
        ...
```

The notifier does not need repository or processor operations.

Similarly, `PaymentProcessor`, `PaymentRepository`, and the application boundaries expose only operations required by their clients.

### Dependency Inversion Principle — DIP

High-level application logic depends on abstractions instead of concrete infrastructure classes.

The use case depends on:

```text
PaymentRepository
PaymentNotifier
PaymentProcessor
```

and not directly on:

```text
InMemoryPaymentRepository
ConsolePaymentNotifier
PixPaymentProcessor
```

Concrete dependencies are created in the composition root and injected into the application.

```text
main.py
   ↓
creates implementations
   ↓
injects dependencies
   ↓
ProcessPaymentUseCase
```

## Composition Root

`main.py` is responsible for assembling the application.

A single repository instance is shared between the process and retrieval use cases:

```python
payment_repository = InMemoryPaymentRepository()

process_payment_use_case = ProcessPaymentUseCase(
    payment_validator=PaymentValidator(),
    payment_repository=payment_repository,
    payment_notifier=ConsolePaymentNotifier(),
    payment_processors=[
        PixPaymentProcessor(),
        CreditCardPaymentProcessor(),
        BankTransferPaymentProcessor(),
    ],
)

get_payment_use_case = GetPaymentUseCase(
    payment_repository=payment_repository,
)
```

The use cases receive their dependencies instead of constructing them internally.

## Payment Processing Flow

```text
POST /api/v1/payments
        ↓
PaymentRequest
        ↓
ProcessPaymentCommand
        ↓
ProcessPaymentUseCase
        ↓
PaymentValidator
        ↓
Payment created
        ↓
PaymentProcessor selected
        ↓
Payment processed
        ↓
PaymentRepository.save()
        ↓
PaymentNotifier.send()
        ↓
PaymentResponse
```

## Supported Payment Methods

The current implementation contains processors for:

* PIX
* Credit Card
* Bank Transfer

Processors are selected dynamically through the `PaymentProcessor` contract.

## API

### Create Payment

```http
POST /api/v1/payments
```

Example request:

```json
{
  "customerId": "3d30a429-74f5-4dd1-b42d-e27c38db42f7",
  "amount": 100.00,
  "currency": "BRL",
  "paymentMethod": "PIX"
}
```

Example response:

```json
{
  "paymentId": "f2ea46df-89ae-4479-8c61-f5895c957124",
  "customerId": "3d30a429-74f5-4dd1-b42d-e27c38db42f7",
  "amount": 100.00,
  "currency": "BRL",
  "paymentMethod": "PIX",
  "status": "APPROVED",
  "createdAt": "2026-07-25T00:00:00Z"
}
```

### Get Payment

```http
GET /api/v1/payments/{payment_id}
```

Returns the payment associated with the provided ID.

## Running the Project

Install dependencies:

```bash
uv sync
```

Start the FastAPI development server:

```bash
uv run fastapi dev
```

Or using another port:

```bash
uv run fastapi dev --port 8001
```

Open the Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

When using port `8001`:

```text
http://127.0.0.1:8001/docs
```

## Tests

Run the complete test suite:

```bash
uv run pytest -v
```

The project contains tests for:

* payment processor contracts
* successful payment processing
* missing payment processor
* invalid payment commands
* successful payment retrieval
* payment not found

Use case tests mock application gateways so that the business flow can be tested independently from infrastructure implementations.

Example:

```text
                    Mock Repository
                         ↑
                         │
Command → ProcessPaymentUseCase → Mock Notifier
                         │
                         ↓
                    Mock Processor
```

## Code Quality

Run Ruff:

```bash
uv run ruff check .
```

## Design Decisions

### Why use a Command?

`PaymentRequest` belongs to the HTTP layer.

Passing it directly into the application would couple the use case to an external representation.

Instead:

```text
PaymentRequest
      ↓
ProcessPaymentCommand
      ↓
ProcessPaymentUseCase
```

The command represents the application's input independently from HTTP.

### Why use Protocol?

`Protocol` allows application contracts to be expressed using Python's typing system.

This project uses explicit inheritance as well:

```python
class InMemoryPaymentRepository(PaymentRepository):
    ...
```

Although Python supports structural typing without explicit inheritance, explicit implementation was chosen here to make architectural relationships easier to identify while studying and reviewing the project.

### Why is Payment not a Pydantic model?

The domain should not depend on the web framework or serialization library.

Pydantic is used at the application boundary for API request and response models, while the domain uses plain Python objects.

### Why use an in-memory repository?

Persistence technology is intentionally not the focus of this project.

Because the application depends on `PaymentRepository`, the in-memory implementation could later be replaced by PostgreSQL, DynamoDB, or another persistence mechanism without changing the use cases.

## Project Evolution

The project was developed incrementally to demonstrate architectural refactoring:

```text
Initial implementation
        ↓
SRP
        ↓
OCP
        ↓
LSP
        ↓
ISP
        ↓
DIP
        ↓
Clean Architecture
```

The initial version intentionally concentrated responsibilities and concrete dependencies.

Each refactoring step progressively introduced separation of concerns, abstractions, dependency inversion, use cases, boundaries, gateways, and architectural layers.

## What This Project Demonstrates

The main purpose of this repository is not to build a production-ready payment platform.

It demonstrates how design principles affect the structure of a Python application:

```text
SOLID
  +
Dependency Inversion
  +
Use Cases
  +
Boundaries
  +
Gateways
  +
Framework-independent Domain
        ↓
Clean Architecture
```
