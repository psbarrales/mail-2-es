from ..repositories.ILLMServicePort import ILLMServicePort
from ..repositories.IDatabaseRepository import IDatabaseRepository
from ..entities.Mail import Mail
from ..entities.Transaction import Transaction
from utils.with_retry import with_retry


class TransactionService:
    llmServicePort: ILLMServicePort = None
    dbRepository: IDatabaseRepository = None

    def __init__(
        self, llmServicePort: ILLMServicePort, dbRepository: IDatabaseRepository
    ) -> None:
        if self.llmServicePort is None:
            self.llmServicePort = llmServicePort
        if self.dbRepository is None:
            self.dbRepository = dbRepository

    @with_retry(retries=3, backoff=5)
    def get_transaction(self, mail: Mail) -> Transaction:
        accounts = self.dbRepository.get_all_accounts()
        tags = self.dbRepository.get_all_tags()
        return self.llmServicePort.extract_transaction(mail.to_str(), accounts, tags)
