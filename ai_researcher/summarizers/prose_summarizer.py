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

    def summarize(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    self.summary_instructions
                ),
                HumanMessage(content=self.document.page_content),
            ]
        )

        model = gpt4

        json_parser = SimpleJsonOutputParser()
        resilient_parser = OutputFixingParser.from_llm(
            parser=json_parser, llm=model, max_retries=1
        )

        chain = prompt | model | resilient_parser

        paragraphs_target = math.ceil(
            model.get_num_tokens(self.document.page_content) / 1100
        )
        response = chain.invoke(
            {
                "paragraphs_target": paragraphs_target,
                "bullets_target": paragraphs_target * 2,
            }
        )
        return response
