from utils.singleton import Singleton
from ..repositories.IDatabaseRepository import IDatabaseRepository
from ..repositories.ILLMAgentPort import ILLMAgentPort
from ..repositories.ISearchRepository import ISearchRepository
from ..entities.Register import Register
from ..entities.ChatMessage import ChatMessage
from ..entities.ToolFunction import ToolFunction
from ..commands.SearchCommand import SearchCommand
from app.tools.AddRegisterTool import AddRegisterTool


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
                name=f"{self.searchRepository.engine}_Manager_Tool",
                description=f"Usefull when you need to manipulate data of {self.searchRepository.engine} using the API",
                method=self.searchRepository.search_command,
            )
        )
        tools.append(
            ToolFunction(
                name="Create_Transactions_Tool",
                description="Use this when you need to create a register from a message",
                method=self.addRegisterTool.run,
            )
        )
        return tools

    def run(self, chat: ChatMessage) -> ChatMessage:
        tools = self.create_tools()
        self.llmAgent.init(tools)
        return self.llmAgent.run(
            chat.message,
            self.searchRepository.engine,
            self.searchRepository.index,
            self.searchRepository.schema.schema_json(),
            accounts=self.databaseRepository.get_all_accounts(),
            tags=self.databaseRepository.get_all_tags(),
        )
        # return self.databaseRepository.create_account(account)
