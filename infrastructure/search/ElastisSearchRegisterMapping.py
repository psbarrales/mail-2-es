from domain.entities.Register import Register
from pydantic.v1 import Field
from typing import Literal


class RegisterMapping(Register):
    id: str = Field(None, alias="id.keyword", description="UUIDv4 identifier")
    direction: Literal["IN", "OUT"] = Field(
        alias="direction.keyword",
        description="Specifies the type of transaction direction, IN for income and OUT for outcome",
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
        alias="transactionType.keyword",
        description="Specifies the type of transaction: 'DEBIT' for purchases or expenses made with a debit card, 'CREDIT' for credit card transactions, 'TRANSFER' for moving funds between accounts, 'DEPOSIT' for adding funds to an account, 'WITHDRAWAL' for taking money out of an account, 'REFUND' for returning funds to an account, 'ADJUSTMENT' for correcting or adjusting account transactions, and 'BUDGET' for transactions related to budgeting purposes.",
    )
    currency: str = Field(
        ...,
        alias="currency.keyword",
        regex=r"^[A-Z]{3}$",
        description="Currency code (ISO 4217)",
    )
