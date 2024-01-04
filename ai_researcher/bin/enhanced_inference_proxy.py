from sse_starlette.sse import EventSourceResponse
import json
import os
import shutil
import xml.etree.ElementTree
from typing import AsyncGenerator

from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_community.callbacks import get_openai_callback
from langchain_core.documents import Document
from langchain_core.exceptions import OutputParserException
from starlette.responses import (
    StreamingResponse,
    AsyncContentStream,
    JSONResponse,
)

from ai_researcher.document_loaders.epub_loader import EPubLoader
from ai_researcher.summarizers.prose_summarizer import ProseSummarizer
from ai_researcher.utils import (
    debug,
    dump_raw,
    dump_json,
    sanitize_filename,
    read_json,
    read_raw,
    copy_file,
)
from fastapi import FastAPI, Request
import httpx
import uvicorn
from openai import AsyncOpenAI, OpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_KEY")

# client = OpenAI(api_key=openai_api_key)
client = AsyncOpenAI(api_key=openai_api_key)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8000",
        "https://www.typingmind.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_api_url = "https://api.openai.com/v1"  # Replace with the actual OpenAI API URL if different

# The client to make async requests to OpenAI API.
http_client = httpx.AsyncClient()


# @app.api_route("/{openai_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
# async def forward_openai_request(request: Request, openai_path: str):
#     # Extract method and body from the original request
#     method = request.method.lower()
#     body = await request.body()
#
#     # Forwarding headers from the original request (you might want to filter or modify these)
#     headers = dict(request.headers)
#
#     # You must include your OpenAI API key in the headers
#     headers["Authorization"] = "Bearer YOUR_OPENAI_API_KEY"
#
#     # Construct the full URL to which we'll forward the request
#     url = f"{openai_api_url}/{openai_path}"
#
#     # Forwarding params from the original request (for GET requests)
#     params = dict(request.query_params)
#
#     # Send the request to OpenAI API and return response back to client
#     response = await http_client.request(
#         method=method, url=url, headers=headers, data=body, params=params
#     )
#
#     return response.json()


# // TODO Sam - len post
@app.api_route("/generate", methods=["GET", "POST", "PUT", "DELETE"])
async def get_generate():
    raw_response = await client.chat.completions.with_raw_response.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": "Say hello",
            }
        ],
        stream=True,
    )

    httpx_response = raw_response.http_response

    async def response_stream():
        try:
            async for chunk in httpx_response.aiter_raw():
                yield chunk
        except Exception as e:
            # Handle exceptions or cleanup here if needed
            raise e

    return StreamingResponse(
        response_stream(),
        headers=dict(httpx_response.headers),
        status_code=httpx_response.status_code,
    )

    return raw_response.http_response

    completion_response = raw_response.parse()
    completion_response_headers = raw_response.headers
    completion_status_code = raw_response.status_code
    # if "content-encoding" in completion_response_headers:
    #     completion_response_headers.pop(
    #         "content-encoding"
    #     )  # Remove "br" that will be changed by this proxy

    async def process_stream(
        stream: AsyncContentStream,
    ) -> AsyncGenerator[str, None]:
        # Async content generator
        try:
            async for chunk in stream:
                if chunk:
                    yield chunk.model_dump_json()
        finally:
            pass

    debug(completion_response)
    debug(completion_response.model.model_dump())
    debug(completion_response.model.model_dump_json())
    debug(process_stream(completion_response))

    return EventSourceResponse(
        process_stream(completion_response),
        headers=completion_response_headers,
        status_code=completion_status_code,
    )

    # return JSONResponse(
    #     content=completion_response.model_dump(),
    #     headers=completion_response_headers,
    # )

    async def process_stream(
        stream: AsyncContentStream,
    ) -> AsyncGenerator[str, None]:
        # Async content generator
        try:
            async for chunk in stream:
                self.access_logger_qrueue.put(
                    ChatGPTStreamResponseItem(
                        request_id=request_id, chunk_json=chunk.model_dump()
                    )
                )
                if chunk:
                    yield chunk.model_dump_json()

        finally:
            # Response log
            now = time.time()
            self.access_logger_queue.put(
                ChatGPTStreamResponseItem(
                    request_id=request_id,
                    response_headers=completion_response_headers,
                    duration=now - start_time,
                    duration_api=now - start_time_api,
                    request_json=request_json,
                    status_code=completion_status_code,
                )
            )

    return self.return_response_with_headers(
        EventSourceResponse(
            process_stream(completion_response),
            headers=completion_response_headers,
        ),
        request_id,
    )


if __name__ == "__main__":
    # // TODO Sam -file watcher
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
