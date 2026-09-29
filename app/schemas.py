from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from decimal import Decimal

class CreateWalletRequest(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    initial_balance: Decimal = 0

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name of wallet is required")
        return value

    @field_validator('initial_balance')
    @classmethod
    def initial_balance_can_not_be_negative(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("Initial balance can't be negative")
        return value



class OperationRequest(BaseModel):
    wallet_name: str = Field(max_length=100)
    amount: Decimal
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