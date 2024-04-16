from utils.singleton import Singleton
from ..repositories.IBotServicePort import IBotServicePort
from typing import Any


class BotService(metaclass=Singleton):
    botServicePort: IBotServicePort = None

    def __init__(self, botServicePort: IBotServicePort) -> None:
        if self.botServicePort is None:
            self.botServicePort = botServicePort

    def start(self, func: Any):
        self.botServicePort.init(func)