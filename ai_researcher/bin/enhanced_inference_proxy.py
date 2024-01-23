import os
from pprint import pprint

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI, OpenAI
from starlette.requests import Request
from starlette.responses import (
    StreamingResponse,
    JSONResponse,
    Response,
)

from ai_researcher.openai_models import OpenAiModels
from ai_researcher.utils import debug

load_dotenv()
# TODO Sam - key should come from typingmind
openai_api_key = os.getenv("OPENAI_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID")

client_oai = AsyncOpenAI(api_key=openai_api_key, organization=openai_org_id)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.typingmind.com",
    ],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


async def streaming_reponse(raw_response):
    httpx_response = raw_response.http_response
    return StreamingResponse(
        httpx_response.aiter_raw(),
        headers=dict(httpx_response.headers),
        status_code=httpx_response.status_code,
    )


async def buffered_response(raw_response):
    return Response(
        content=raw_response.content,
        headers={
            k: v
            for k, v in raw_response.headers.items()
            if k.lower()
            not in ["content-length", "transfer-encoding", "content-encoding"]
        },
        status_code=raw_response.status_code,
    )


@app.post("{openai_path:path}")
async def proxy_inference(request: Request):
    request_body = await request.json()

    overriden_args = ["model"]
    completion_args = {
        k: v for k, v in request_body.items() if k not in overriden_args
    }

    # ignore:
    #     model
    #
    # modify:
    #     messages
    #     tools
    #     tool_choice
    #     ? response_format json
    #
    # forward:
    #     stream
    #     temperature
    #     presence_penalty
    #     frequency_penalty
    #     top_p
    #
    # mozem ja doplnit:
    #     seed
    #     stop
    #     logit_bias
    #     logprobs
    #     top_logprobs

    raw_response = await client_oai.chat.completions.with_raw_response.create(
        **completion_args,
        model=OpenAiModels.GPT_4_TURBO.value,
    )

    if request_body.get("stream") is True:
        return await streaming_reponse(raw_response)
    else:
        return await buffered_response(raw_response)


def start_webserver():
    uvicorn.run(
        "ai_researcher.bin.enhanced_inference_proxy:app",
        host="127.0.0.1",
        port=4242,
        reload=True,  # reloads on file changes
    )


if __name__ == "__main__":
    start_webserver()
