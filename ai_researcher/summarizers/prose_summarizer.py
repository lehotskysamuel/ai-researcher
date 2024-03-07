import math

from langchain.output_parsers import OutputFixingParser
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)

from ai_researcher.openai_models import gpt4


class ProseSummarizer:
    def __init__(self, document: Document, summary_instructions: str):
        self.document = document
        self.summary_instructions = summary_instructions
        self.model = gpt4

    def summarize(
        self, paragraphs_target: int = None, bullets_target: int = None
    ):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    self.summary_instructions
                ),
                HumanMessage(content=self.document.page_content),
            ]
        )

        json_parser = SimpleJsonOutputParser()
        resilient_parser = OutputFixingParser.from_llm(
            parser=json_parser, llm=self.model, max_retries=1
        )

        chain = prompt | self.model | resilient_parser

        if paragraphs_target is None:
            paragraphs_target = math.ceil(
                self.model.get_num_tokens(self.document.page_content) / 1650
            )
        if bullets_target is None:
            bullets_target = paragraphs_target * 2

        response = chain.invoke(
            {
                "paragraphs_target": paragraphs_target,
                "bullets_target": bullets_target,
            }
        )
        return response
