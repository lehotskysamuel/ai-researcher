import os

from dotenv import load_dotenv
from langchain.llms import OpenAI


load_dotenv()


def main():
    openai_api_key = os.getenv("OPENAI_KEY")

    llm = OpenAI(api_key=openai_api_key)
    response = llm.invoke("Hello, World!")

    print(response)


if __name__ == "__main__":
    main()
