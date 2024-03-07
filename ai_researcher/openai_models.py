import os
from enum import Enum

from aiolimiter import AsyncLimiter
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


class OpenAiChatModels(Enum):
    GPT_4_TURBO = "gpt-4-0125-preview"
    GPT_4_VISION = "gpt-4-vision-preview"
    GPT_3_5_TURBO = "gpt-3.5-turbo-1106"


class OpenAiEmbeddingModels(Enum):
    V3_LARGE = "text-embedding-3-large"
    V3_SMALL = "text-embedding-3-small"


load_dotenv()
openai_api_key = os.getenv("OPENAI_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID")

gpt4 = ChatOpenAI(
    openai_api_key=openai_api_key,
    openai_organization=openai_org_id,
    model_name=OpenAiChatModels.GPT_4_TURBO.value,
)

gpt4_vision = ChatOpenAI(
    api_key=openai_api_key,
    openai_organization=openai_org_id,
    model_name=OpenAiChatModels.GPT_4_VISION.value,
)

gpt3 = ChatOpenAI(
    api_key=openai_api_key,
    openai_organization=openai_org_id,
    model_name=OpenAiChatModels.GPT_3_5_TURBO.value,
)

embeddings = OpenAIEmbeddings(
    # 3072 dimensions
    api_key=openai_api_key,
    openai_organization=openai_org_id,
    model=OpenAiEmbeddingModels.V3_LARGE.value,
)

embeddings_sm = OpenAIEmbeddings(
    # 1536 dimensions
    api_key=openai_api_key,
    openai_organization=openai_org_id,
    model=OpenAiEmbeddingModels.V3_SMALL.value,
)

# TODO refactor to a class
# TODO also tokens per minute
embeddings_rate_limiter = AsyncLimiter(500, 60)  # 500 requests per minute
