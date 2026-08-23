from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import uuid
import datetime

app = FastAPI(
    title="FinTrust Transaction API",
    version="1.0.0"
)

# -------------------------
# Middleware
# -------------------------
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

app.add_middleware(RequestIDMiddleware)

# -------------------------
# Models
# -------------------------
class TransactionIn(BaseModel):
    account_id: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    currency: str = Field(..., pattern=r'^[A-Z]{3}$')
    description: Optional[str] = None

    @validator("amount")
    def amount_max(cls, value):
        if value > 1_000_000:
            raise ValueError(
                "Amount exceeds single-transaction limit of 1,000,000"
            )
        return value


class TransactionOut(TransactionIn):
    id: str
    status: str
    created_at: str


class StatusUpdate(BaseModel):
    status: str

    @validator("status")
    def validate_status(cls, value):
        allowed = ["approved", "rejected"]
        if value not in allowed:
            raise ValueError(
                "Status must be either 'approved' or 'rejected'"
            )
        return value


transactions: List[dict] = []

# -------------------------
# Existing Endpoints
# -------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post(
    "/transactions",
    response_model=TransactionOut,
    status_code=201
)
async def create_transaction(body: TransactionIn):
    txn = {
        "id": str(uuid.uuid4()),
        **body.dict(),
        "status": "pending",
        "created_at": datetime.datetime.utcnow().isoformat()
    }

    transactions.append(txn)
    return txn


@app.get(
    "/transactions",
    response_model=List[TransactionOut]
)
async def list_transactions(
    account_id: Optional[str] = Query(None)
):
    if account_id:
        return [
            t for t in transactions
            if t["account_id"] == account_id
        ]
    return transactions


# -------------------------
# Extension Feature 1
# GET /transactions/{id}
# -------------------------
@app.get(
    "/transactions/{id}",
    response_model=TransactionOut
)
async def get_transaction(id: str):
    for txn in transactions:
        if txn["id"] == id:
            return txn

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )


# -------------------------
# Extension Feature 2
# PATCH /transactions/{id}/status
# -------------------------
@app.patch(
    "/transactions/{id}/status",
    response_model=TransactionOut
)
async def update_status(
    id: str,
    body: StatusUpdate
):
    for txn in transactions:
        if txn["id"] == id:
            txn["status"] = body.status
            return txn

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )