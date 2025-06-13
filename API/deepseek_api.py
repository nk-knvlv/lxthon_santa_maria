import json

import requests

import config


class SantaMariaAI:
    """
    Класс Api для удобной работы с DeepSeek
    """

    def __new__(cls, *args, **kwargs):
        """
        Контролирует Инициализацию класса
        :param args:
        :param kwargs:
        """
        if 'api_key' not in kwargs:
            raise ValueError("The Api key cannot be empty")
        if "system_prompt" not in kwargs:
            kwargs["system_prompt"] = ''
        return super().__new__(cls)

    def __init__(self, *, api_key: str, system_prompt='') -> None:
        if api_key is None:
            raise ValueError("The Api key cannot be empty")
        self.API_KEY = api_key
        self.MODEL = "deepseek/deepseek-r1"
        self.messages = [{"role": "user", "content": system_prompt}]
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def run(self, prompt: str) -> str:
        """
        Выполняет Запрос
        :param prompt:
        :return:
        """
        self.messages.append({"role": "user", "content": prompt})
        data = {
            "model": self.MODEL,
            "messages": self.messages,
            "stream": True
        }

        with requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=self.headers,
                json=data,
                stream=True) as response:
            if response.status_code != 200:
                print("Ошибка API:", response.status_code)
                return ""
            full_response = []

            for chunk in response.iter_lines():
                if chunk:
                    chunk_str = chunk.decode('utf-8').replace('data: ', '')
                    try:
                        chunk_json = json.loads(chunk_str)
                        if "choices" in chunk_json:
                            content = chunk_json["choices"][0]["delta"].get("content", "")
                            if content:
                                print(content, end='', flush=True)
                                full_response.append(content)
                    except json.decoder.JSONDecodeError:
                        pass
                    except Exception as error:
                        print(error)
            self.messages.append({'role': 'assistant', 'content': ''.join(full_response)})
            return ''.join(full_response)



