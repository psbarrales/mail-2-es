from ..entities.Transaction import Transaction
from ..entities.Register import Register
from ..entities.Account import Account
from ..entities.Mail import Mail
from ..entities.Tag import Tag
from ..repositories.IDatabaseRepository import IDatabaseRepository
from ..repositories.ILLMServicePort import ILLMServicePort
from ..repositories.ISearchRepository import ISearchRepository
from typing import List
from dateutil.relativedelta import relativedelta
from uuid import uuid4
from utils.with_retry import with_retry
import copy


class RegisterService:
    llmServicePort: ILLMServicePort = None
    dbRepository: IDatabaseRepository = None
    searchRepository: ISearchRepository = None

    def __init__(
        self,
        llmServicePort: ILLMServicePort,
        searchRepository: ISearchRepository,
        dbRepository: IDatabaseRepository,
    ) -> None:
        if self.llmServicePort is None:
            self.llmServicePort = llmServicePort
        if self.searchRepository is None:
            self.searchRepository = searchRepository
        if self.dbRepository is None:
            self.dbRepository = dbRepository

    @with_retry(retries=3, backoff=5)
    def get_transaction(self, mail: Mail) -> Transaction:
        accounts = self.dbRepository.get_all_accounts()
        tags = self.dbRepository.get_all_tags()
        return self.llmServicePort.extract_transaction(mail.to_str(), accounts, tags)

    def create_registers(self, transaction: Transaction) -> List[Register]:
        registers: List[Register] = []
        # Get the account
        account = self.dbRepository.find_account_by_id(int(transaction.accountId))
        tags = [Tag(tag=tag_name.upper()) for tag_name in transaction.tags]
        # Get transaction type
        type = transaction.transactionType
        uuid = str(uuid4())
        transaction_date = copy.deepcopy(transaction.date)
        transaction_billDate = copy.deepcopy(transaction.billDate)
        if account.billDay is not None and account.billDay > 0:
            billDay = account.billDay
            nextBillDay = (
                transaction_date.replace(day=billDay)
                if transaction_date.day < billDay
                and transaction_date.month == transaction_billDate.month
                else transaction_date.replace(day=billDay) + relativedelta(months=+1)
            )
            nextBillDay = nextBillDay.replace(hour=7, minute=0, second=0, microsecond=0)
            transaction_billDate = copy.deepcopy(nextBillDay)

        if type in ["DEBIT", "DEPOSIT", "WITHDRAWAL", "REFUND", "ADJUSTMENT", "BUDGET"]:
            quotas = int(1 if transaction.quotas <= 1 else transaction.quotas)
            registers.append(
                Register(
                    id=uuid,
                    description=f"{transaction.description}"
                    + (f"(Repetición 1 de {quotas})" if quotas > 1 else ""),
                    transactionType=type,
                    direction=transaction.direction,
                    amount=transaction.amount,
                    currency=transaction.currency,
                    tags=tags,
                    account=account,
                    date=transaction_date,
                    billDate=transaction_billDate,
                )
            )
            if quotas > 1:
                nextRepetitionDay = transaction_date + relativedelta(months=+1)
                nextRepetitionBillDay = transaction_billDate + relativedelta(months=+1)
                repetitionDate = copy.deepcopy(nextRepetitionDay)
                repetitionBillDate = copy.deepcopy(nextRepetitionBillDay)
                for quota in range(2, quotas + 1):
                    registers.append(
                        Register(
                            id=uuid,  # Unique ID for each register
                            description=f"{transaction.description} (Repetición {quota} de {quotas})",
                            transactionType=type,
                            direction=transaction.direction,
                            amount=transaction.amount,
                            currency=transaction.currency,
                            tags=tags,
                            account=account,
                            date=copy.deepcopy(repetitionDate),
                            billDate=copy.deepcopy(repetitionBillDate),
                        )
                    )
                    repetitionDate += relativedelta(months=+1)
                    repetitionBillDate += relativedelta(months=+1)

        if type == "CREDIT":
            quotas = int(1 if transaction.quotas <= 1 else transaction.quotas)
            amount = transaction.amount / quotas
            billDate = copy.deepcopy(transaction_billDate)
            for quota in range(1, quotas + 1):
                registers.append(
                    Register(
                        id=uuid,
                        description=f"{transaction.description} (Cuota {quota} de {quotas})",
                        transactionType=type,
                        direction=transaction.direction,
                        amount=amount,
                        currency=transaction.currency,
                        tags=tags,
                        account=account,
                        quotas=float(quota),
                        date=transaction.date,
                        billDate=copy.deepcopy(billDate),
                        isBilled=False,
                        isPayed=False,
                    )
                )
                billDate += relativedelta(months=+1)

        if type == "TRANSFER":
            destinationAccount: Account = None
            if transaction.destinationAccountId is not None:
                destinationAccount = self.dbRepository.find_account_by_id(
                    int(transaction.destinationAccountId)
                )
            if account.id != 99:
                source = Register(
                    id=uuid,
                    description=transaction.description,
                    transactionType=type,
                    direction=transaction.direction,
                    amount=transaction.amount,
                    currency=transaction.currency,
                    tags=tags,
                    account=account,
                    destinationAccount=destinationAccount,
                    date=transaction.date,
                    billDate=transaction.billDate,
                )
                registers.append(source)
            if (
                destinationAccount is not None
                and destinationAccount.id != 99
                and account.id != destinationAccount.id
            ):
                target = Register(
                    id=uuid,
                    description=("<- " if transaction.direction == "IN" else "-> ") + transaction.description,
                    transactionType=type,
                    direction="OUT" if transaction.direction == "IN" else "IN",
                    amount=transaction.amount,
                    currency=transaction.currency,
                    tags=tags,
                    account=destinationAccount,
                    destinationAccount=account,
                    date=transaction.date,
                    billDate=transaction.billDate,
                )
                registers.append(target)

        self.searchRepository.store_register(registers)
        return registers
