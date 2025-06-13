import time
from uuid import uuid4

import urllib3
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_gigachat.chat_models import GigaChat

import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class SpaceWorldAGI:
    def __init__(self, API_KEY: str, SYSTEM_PROMPT: str):
        self.giga = GigaChat(
            credentials="N2E0MGU0NjctOGFiOS00NTAxLTg4OWEtMGZhODk2NzRmNWZmOmY3YmE0NmFkLTIyYzQtNDQ4YS1iMzQ2LWRkZGQzNDkxOTk1Nw==",
            verify_ssl_certs=False,
            timeout=30
        )

        self.system_template = SYSTEM_PROMPT
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_template),
            ("human", "{input}")
        ])

        self.messages = [SystemMessage(content=self.system_template)]

    def run(self, user_input):
        """Основной цикл взаимодействия"""
        print("SpaceWorld AGI активирован. Ожидание запроса...")
        try:
            self.messages.append(HumanMessage(content=user_input))
            response = self.giga.invoke(self.messages)
            self.messages.append(response.content)
            return response.content

        except Exception as e:
            print(f"\nОШИБКА СИСТЕМЫ: {str(e)}")
            time.sleep(1)

