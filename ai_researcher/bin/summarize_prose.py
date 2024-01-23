import json
import os
import shutil
import xml.etree.ElementTree

from langchain_community.callbacks import get_openai_callback
from langchain_core.documents import Document
from langchain_core.exceptions import OutputParserException

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

# load_dotenv()


def process_book(book_path):
    loader = EPubLoader(book_path)
    documents = loader.load()

    book_folder = sanitize_filename(loader.title)
    data_folder = f"data/documents/books/raw/{book_folder}"

    dump_json(
        {
            "title": loader.title,
            "authors": loader.authors,
            "items_length": loader.items_length,
            "file_name": os.path.basename(book_path),
        },
        f"{data_folder}/metadata.json",
    )

    for i, doc in enumerate(documents):
        destination = f"{data_folder}/doc_{i}.json"
        dump_json(
            {"page_content": doc.page_content, "metadata": doc.metadata},
            destination,
        )

    return book_folder


def import_book_dump(book_folder):
    metadata = read_json(f"{book_folder}/metadata.json")
    docs = []

    for i in range(metadata["items_length"]):
        doc_path = f"{book_folder}/doc_{i}.json"
        doc_json = read_json(doc_path)
        docs.append(
            Document(
                page_content=doc_json["page_content"],
                metadata=doc_json["metadata"],
            )
        )

    return docs, metadata


def summarize(book_folder):
    documents, metadata = import_book_dump(
        f"data/documents/books/raw/{book_folder}"
    )

    copy_file(
        f"data/documents/books/raw/{book_folder}/metadata.json",
        f"data/documents/books/summaries/{book_folder}/metadata.json",
    )

    with get_openai_callback() as cb:
        for i, doc in enumerate(documents):
            print(f"In Progress: Item #{i}")
            summarizer = ProseSummarizer(doc)

            try:
                summary = summarizer.summarize()
                dump_json(
                    summary,
                    f"data/documents/books/summaries/{book_folder}/summary_{i}.json",
                )
            except OutputParserException as e:
                dump_raw(
                    e.llm_output,
                    f"data/documents/books/summaries/{book_folder}/summary_{i}.fallback.txt",
                )
            except Exception as e:
                try:
                    dump_raw(
                        str(e),
                        f"data/documents/books/summaries/{book_folder}/summary_{i}.error.txt",
                    )
                except:
                    pass

        print(cb)


def main():
    # process_book("C:\\Users\\lehot\\Downloads\\dawnoffireavengingson.epub")
    summarize("dawn of fire - avenging son")
    # process_book("C:\\Users\\lehot\\Downloads\\lordsofsilence.epub")
    # summarize("the lords of silence")


if __name__ == "__main__":
    main()
