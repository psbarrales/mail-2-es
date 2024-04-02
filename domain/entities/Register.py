from pydantic.v1 import BaseModel, Field
from typing import Sequence, Literal, Optional
from datetime import datetime
from uuid import uuid4
from .Account import Account
from .Tag import Tag


class Register(BaseModel):
    id: str = Field(str(uuid4()))
    tags: Sequence[Tag] = Field(
        ..., description="Extract, create tags from the transaction. At least 3"
    )
    account: Account = Field(..., description="Account ID for the source")
    direction: Literal["IN", "OUT"] = Field(
        description="Specifies the type of transaction direction, IN for income and OUT for outcome"
    )
    transactionType: Literal[
        "DEBIT",
        "CREDIT",
        "TRANSFER",
        "DEPOSIT",
        "WITHDRAWAL",
        "REFUND",
        "ADJUSTMENT",
        "BUDGET",
    ] = Field(
        description="Specifies the type of transaction: 'DEBIT' for purchases or expenses made with a debit card, 'CREDIT' for credit card transactions, 'TRANSFER' for moving funds between accounts, 'DEPOSIT' for adding funds to an account, 'WITHDRAWAL' for taking money out of an account, 'REFUND' for returning funds to an account, 'ADJUSTMENT' for correcting or adjusting account transactions, and 'BUDGET' for transactions related to budgeting purposes."
    )
    currency: str = Field(
        ...,
        regex=r"^[A-Z]{3}$",
        description="Currency code (ISO 4217)",
    )
    amount: float = Field(
        ...,
        gt=0,
        description="Amount of transaction. Must be greater than 0. When USD use decimal value",
    )
    quotas: Optional[float] = Field(
        None, description="Number of quotas for Credit transaction type."
    )
    description: str = Field(
        ..., min_length=1, max_length=1024, description="Description of the transaction"
    )
    date: datetime = Field(
        description="Date of transaction. Format ISO (YYYY-MM-DDThh:mm:ss)"
    )
    billDate: datetime = Field(
        description="Date of billing, normally same as date, per credit should be different. Format ISO (YYYY-MM-DDThh:mm:ss)"
    )
    destinationAccount: Optional[Account] = Field(
        None, description="Target Account Name for the target if transfer type"
    )
    isBilled: bool = Field(default=True)
    isPayed: bool = Field(default=True)
    isBudget: bool = Field(default=False)
    isSaving: bool = Field(default=False)
