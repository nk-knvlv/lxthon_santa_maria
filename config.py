from decouple import config

VEXA_API_KEY = config("VEXA_API_KEY")
AI_API_KEY = config("API_KEY")

SYSTEM_PROMPT = """Привет. Ты нейро-сетевой агент помощник в google meet. 
Твоя задача по предоставленному логу чата с пользователями, временем и сообщениям отправить краткое содержание диалога.
Больше ничего от тебя не нужно"""
