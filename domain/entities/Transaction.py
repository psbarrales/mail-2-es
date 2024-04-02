from pydantic.v1 import BaseModel, Field
from typing import Sequence, Literal
from datetime import datetime


class Transaction(BaseModel):
    tags: Sequence[str] = Field(
        ..., description="Extract, create tags from the transaction. At least 3"
    )
    accountId: str = Field(
        ..., description="Account ID that get the transaction movement"
    )
    accountName: str = Field(
        ..., description="Account Name that get the transaction movement"
    )
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
    quotas: float = Field(
        ..., description="Number of quotas for Credit transaction type."
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
    destinationAccountId: str = Field(
        ...,
        description="Target Account ID for the target if transfer type or secondary account",
    )
    destinationAccountName: str = Field(
        ...,
        description="Target Account Name for the target if transfer type or secondary account",
    )
