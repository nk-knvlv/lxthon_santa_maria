from typing import Union, List

from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_gigachat.chat_models import GigaChat


class GigaChatAPI:
    """
    Класс для работы с нейросетью GigaChat API
    """
    __slots__ = ["giga", "system_template", "prompt_template", "messages"]

    def __init__(self,
                 API_KEY: str,
                 SYSTEM_PROMPT: str):
        """
        Инициализация модели
        :param API_KEY: API ключ GigaChat API
        :param SYSTEM_PROMPT: Системный промт нейросети
        """
        self.giga: GigaChat = GigaChat(
            credentials=API_KEY,
            verify_ssl_certs=False,
            timeout=30
        )

        self.system_template: str = SYSTEM_PROMPT
        self.prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_messages([
            ("system", self.system_template),
            ("human", "{input}")
        ])
        self.messages: List[Union[SystemMessage, HumanMessage]] = [SystemMessage(content=self.system_template)]

    def run(self, user_input: str) -> Union[str, List[Union[str, dict]]]:
        """
        Выполняет запрос нейросети
        :param user_input: Входной запрос пользователя
        :return: Ответ от нейросети
        """
        try:
            self.messages.append(HumanMessage(content=user_input))
            response: BaseMessage = self.giga.invoke(self.messages)
            self.messages.append(SystemMessage(content=response.content))
            return response.content
        except Exception as e:
            print(f"\nERROR: {e}")
