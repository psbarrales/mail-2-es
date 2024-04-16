from domain.entities.ChatMessage import ChatMessage
from domain.services.AgentService import AgentService
from domain.services.BotService import BotService
from infrastructure.database.sql.SQLAlchemyAdapter import SQLAlchemyAdapter
from infrastructure.llm.OpenAILLMAgent import OpenAILLMAgent
from infrastructure.search.ElasticSearchRepository import ElasticSearchRepository
from infrastructure.notification.TelegramBot import TelegramBot


class AgentServices:
    agentService: AgentService = None
    botService: BotService = None

    def __init__(self) -> None:
        if self.agentService is None:
            self.agentService = AgentService(
                OpenAILLMAgent(), ElasticSearchRepository(), SQLAlchemyAdapter()
            )
        if self.botService is None:
            self.botService = BotService(TelegramBot())

    def bot(self) -> None:
        self.botService.start(self.chat)

    def chat(self, message: str) -> ChatMessage:
        chat = ChatMessage(message=message)
        return self.agentService.run(chat)
