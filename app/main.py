from fastapi import FastAPI

app = FastAPI(title="Payment Service",
              version="0.1.0")


@app.get("/healthcheck")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
