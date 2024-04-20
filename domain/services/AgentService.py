from utils.singleton import Singleton
from ..repositories.IDatabaseRepository import IDatabaseRepository
from ..repositories.ILLMAgentPort import ILLMAgentPort
from ..repositories.ISearchRepository import ISearchRepository
from ..entities.ChatMessage import ChatMessage
from ..entities.ToolFunction import ToolFunction
from app.tools.AddRegisterTool import AddRegisterTool
from utils.with_retry import with_retry


class AgentService(metaclass=Singleton):
    llmAgent: ILLMAgentPort = None
    searchRepository: ISearchRepository = None
    databaseRepository: IDatabaseRepository = None

    def __init__(
        self,
        llmAgent: ILLMAgentPort,
        searchRepository: ISearchRepository,
        databaseRepository: IDatabaseRepository,
    ) -> None:
        if self.llmAgent is None:
            self.llmAgent = llmAgent
        if self.searchRepository is None:
            self.searchRepository = searchRepository
        if self.databaseRepository is None:
            self.databaseRepository = databaseRepository
        self.addRegisterTool = AddRegisterTool()

    def create_tools(self):
        tools = []
        tools.append(
            ToolFunction(
                name=f"{self.searchRepository.engine}_API_Tool",
                description=f"Usefull when you need to manipulate data of {self.searchRepository.engine} using the API",
                method=self.searchRepository.search_command,
            )
        )
        tools.append(
            ToolFunction(
                name="Create_Transaction_Tool",
                description="Use this to create a register from a plain text, try to get every details for a Register before create the message to be converted to transaction",
                method=self.addRegisterTool.run,
            )
        )
        return tools

    @with_retry(retries=3, backoff=30)
    def run(self, chat: ChatMessage) -> ChatMessage:
        # Connect to databases (start databases)
        self.searchRepository.is_connected()
        self.databaseRepository.get_all_accounts()

        self.llmAgent.init(self.create_tools())
        return self.llmAgent.run(
            chat.message,
            self.searchRepository.engine,
            self.searchRepository.index,
            self.searchRepository.schema.schema_json(),
            accounts=self.databaseRepository.get_all_accounts(),
            tags=self.databaseRepository.get_all_tags(),
        )
        # return self.databaseRepository.create_account(account)
