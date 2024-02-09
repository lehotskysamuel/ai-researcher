import os
import random
import time
from typing import List, Union

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from ai_researcher.utils import debug

load_dotenv()
openai_api_key = os.getenv("OPENAI_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# Step 1
class Step1Input(BaseModel):
    user_query: str


class Step1Output(BaseModel):
    search_queries: List[str]


# Step 2
class SearchEngineConfig(BaseModel):
    search_engine: str
    max_results: int


class Step2Input(BaseModel):
    search_queries: List[str]
    search_engine_configs: List[SearchEngineConfig]


class SearchResult(BaseModel):
    search_engine: str
    url: str
    title: str
    description: str


class Step2Output(BaseModel):
    search_results: List[SearchResult]


# TODO Sam - Embedding stranok by mal vygenerovat unikatne ID toho searchu (a dat tam aj datum). Potom sa mozem s tymto ID referencovat na tento search a chatovat vyhradne so strankami z tohto searchu (keby som nahodou nechcel chatovat s celou knowledge base)
# Step 3
class Step3Input(BaseModel):
    url: str


class Step3SuccessOutput(BaseModel):
    success: bool = Field(default=True)
    content: str

    @field_validator("success")
    def set_success_to_true(cls, v):
        return True


class Step3FailureOutput(BaseModel):
    success: bool = Field(default=False)
    error: str

    @field_validator("success")
    def set_success_to_false(cls, v):
        return False


@app.post("/api/search-wizard/step1")
def step1_endpoint(body: Step1Input) -> Step1Output:
    debug(body)
    time.sleep(1)
    return Step1Output(
        search_queries=[
            f"search query 1 {time.time()}",
            "search query 2",
            "search query 3",
        ]
    )


@app.post("/api/search-wizard/step2")
def step2_endpoint(body: Step2Input) -> Step2Output:
    debug(body)
    time.sleep(1)
    results = [
        {
            "search_engine": "Google",
            "title": "Example Title 1",
            "url": "http://example.com",
            "description": "Example Description. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Ut tempus purus at lorem.",
        },
        {
            "search_engine": "Bing",
            "title": "Example Title 2",
            "url": "http://example.com",
            "description": "Example Description. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Ut tempus purus at lorem.",
        },
        {
            "search_engine": "Google",
            "title": "Example Title 3",
            "url": "http://example2.com",
            "description": "Example Description. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Ut tempus purus at lorem.",
        },
    ]
    return Step2Output(search_results=results)


@app.post("/api/search-wizard/step3")
def step3_endpoint(
    body: Step3Input,
) -> Union[Step3SuccessOutput, Step3FailureOutput]:
    time.sleep(1)
    success = random.randint(0, 1) == 1
    if success:
        return Step3SuccessOutput(content="<strong>Successful</strong>")
    else:
        return Step3FailureOutput(error="Network Error: Stack trace...")


def start_webserver():
    uvicorn.run(
        "ai_researcher.bin.main:app",
        host="127.0.0.1",
        port=8080,
    )


if __name__ == "__main__":
    start_webserver()
