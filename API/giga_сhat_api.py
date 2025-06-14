import logging
from typing import Union, List

from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_gigachat.chat_models import GigaChat


class GigaChatAPI:
    """
    A class for working with the Giga Chat API neural network
    """
    __slots__ = ["giga", "system_template", "prompt_template", "messages"]

    def __init__(self,
                 API_KEY: str,
                 SYSTEM_PROMPT: str):
        """
        Initializing the model
        :param API_KEY: API GigaChat API key
        :param SYSTEM_PROMPT: Neural network system promt
        """
        logging.debug("GigaChatAPI init")
        self.giga: GigaChat = GigaChat(
            credentials=API_KEY,
            verify_ssl_certs=False,
            timeout=30
        )
        logging.debug(f"SYSTEM_PROMPT={SYSTEM_PROMPT}")
        self.system_template: str = SYSTEM_PROMPT
        self.prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_messages([
            ("system", self.system_template),
            ("human", "{input}")
        ])
        self.messages: List[Union[SystemMessage, HumanMessage, AIMessage]] = [SystemMessage(content=self.system_template)]

    def run(self, user_input: str) -> Union[str, List[Union[str, dict]]]:
        """
        Executes a neural network query
        :param user_input: User input request
        :return: Response from the neural network
        """
        try:
            self.messages.append(HumanMessage(content=user_input))
            logging.error(f"CREATE REQWESTS USER: {user_input}")
            response: BaseMessage = self.giga.invoke(self.messages)
            print(type(response))
            self.messages.append(AIMessage(content=response.content))
            return response.content
        except Exception as error:
            logging.error(f"ERROR IN REQWESTS TO AI: {error}")
