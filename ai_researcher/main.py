import os
import sys

from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ai_researcher.document_loaders.epub_loader import (
    EPubLoader,
)
from ai_researcher.utils import debug

load_dotenv()


def main():
    # sys.argv[1]
    openai_api_key = os.getenv("OPENAI_KEY")

    path = "C:\\Users\\lehot\\Downloads\\lordsofsilence.epub"

    loader = EPubLoader(path)
    [print(document.page_content) for document in loader.load()]

    # llm = OpenAI(api_key=openai_api_key)
    # response = llm.invoke("Hello, World!")
    # print(response)


if __name__ == "__main__":
    main()
