from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import (
    BaseModel,
    Field,
    field_validator
)

app = FastAPI()

BALANCE = {

}

class CreateWalletRequest(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    initial_balance: float = 0

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name of wallet is required")
        return value

    @field_validator('initial_balance')
    @classmethod
    def initial_balance_can_not_be_negative(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Initial balance can't be negative")
        return value


class OperationRequest(BaseModel):
    wallet_name: str = Field(max_length=100)
    amount: float
    description: str | None = Field(None, max_length=255)


    @field_validator('wallet_name')
    @classmethod
    def wallet_name_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name of wallet is required")
        return value

    @field_validator('amount')
    @classmethod
    def amount_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Amount must be greater than zero")
        return value


@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    if wallet_name is None:


        
        return {"total_balance": sum(BALANCE.values())}
    if wallet_name not in BALANCE:
        raise HTTPException(status_code=404, detail=f"Wallet '{wallet_name}' not found")
    return {"wallet": wallet_name, "balance": BALANCE[wallet_name]}


@app.post("/wallets/{name}")
def create_wallet(wallet: CreateWalletRequest):
    if wallet.name in BALANCE:
        raise HTTPException(status_code=400, detail=f"Wallet '{wallet.name}' already exists")
    BALANCE[wallet.name] = wallet.initial_balance
    return {
        "message": f"Wallet {wallet.name} created",
        "wallet": wallet.name,
        "balance": BALANCE[wallet.name]
    }


@app.post("/operations/income")
def add_income(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(status_code=404, detail=f"Wallet '{operation.wallet_name}' not found")
    if operation.amount <= 0:
        raise HTTPException(
            status_code=400, detail="Amount must be positive"
        )

    BALANCE[operation.wallet_name] += operation.amount
    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }



@app.post("/operations/expense/")
def add_expense(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(status_code=404, detail=f"Wallet '{operation.wallet_name}' not found")
    if BALANCE[operation.wallet_name] < operation.amount:
        raise HTTPException(
            status_code=400, detail=f"Insufficient funds. Available: {BALANCE[operation.wallet_name]}"
        )

    BALANCE[operation.wallet_name] -= operation.amount
    return {
        "message": "Expense added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }
