import os
from enum import Enum

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI


class OpenAIModels(Enum):
    GPT_4_TURBO = "gpt-4-1106-preview"
    GPT_4_VISION = "gpt-4-vision-preview"
    GPT_3_5_TURBO = "gpt-3.5-turbo-1106"


load_dotenv()
openai_api_key = os.getenv("OPENAI_KEY")

gpt4 = ChatOpenAI(
    api_key=openai_api_key,
    model_name=OpenAIModels.GPT_4_TURBO.value,
)

gpt4_vision = ChatOpenAI(
    api_key=openai_api_key,
    model_name=OpenAIModels.GPT_4_VISION.value,
)

gpt3 = ChatOpenAI(
    api_key=openai_api_key, model_name=OpenAIModels.GPT_3_5_TURBO.value
)
