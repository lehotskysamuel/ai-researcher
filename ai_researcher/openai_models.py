import os
from enum import Enum

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI


class OpenAiModels(Enum):
    GPT_4_TURBO = "gpt-4-0125-preview"
    GPT_4_VISION = "gpt-4-vision-preview"
    GPT_3_5_TURBO = "gpt-3.5-turbo-1106"


load_dotenv()
openai_api_key = os.getenv("OPENAI_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID")

gpt4 = ChatOpenAI(
    openai_api_key=openai_api_key,
    openai_organization=openai_org_id,
    model_name=OpenAiModels.GPT_4_TURBO.value,
)

gpt4_vision = ChatOpenAI(
    api_key=openai_api_key,
    openai_organization=openai_org_id,
    model_name=OpenAiModels.GPT_4_VISION.value,
)

gpt3 = ChatOpenAI(
    api_key=openai_api_key,
    openai_organization=openai_org_id,
    model_name=OpenAiModels.GPT_3_5_TURBO.value,
)
