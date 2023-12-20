import os
from enum import Enum

import streamlit as st

from ai_researcher.document_loaders.epub_loader import EPubLoader
from ai_researcher.utils import read_raw, read_json


summaries_folder = "data/documents/books/summaries"


class DocStatus(Enum):
    DICT = "DICT"
    TEXT = "TEXT"
    ERROR = "ERROR"
    MISSING = "MISSING"


def load_documents(book_folder, items_length):
    docs = []
    for i in range(items_length):
        try:
            doc = read_json(
                f"{summaries_folder}/{book_folder}/summary_{i}.json"
            )
            docs.append((DocStatus.DICT, doc))
        except FileNotFoundError:
            try:
                doc = read_raw(
                    f"{summaries_folder}/{book_folder}/summary_{i}.fallback.txt"
                )
                docs.append((DocStatus.TEXT, doc))
            except FileNotFoundError:
                try:
                    doc = read_raw(
                        f"{summaries_folder}/{book_folder}/summary_{i}.error.txt"
                    )
                    docs.append((DocStatus.ERROR, doc))
                except FileNotFoundError:
                    docs.append((DocStatus.MISSING, None))
    return docs


def render(book_folder):
    if book_folder is None:
        st.header("Select a book in the sidebar")
        return

    metadata = read_json(f"{summaries_folder}/{book_folder}/metadata.json")

    st.title(metadata["title"])
    authors = authors_to_string(metadata["authors"])
    st.text(authors)

    items_length = 30

    documents = load_documents(book_folder, items_length)

    st.markdown("## Short Summary")
    for index, (status, doc) in enumerate(documents):
        if status == DocStatus.DICT and doc["relevant"]:
            if doc["title"] is not None:
                st.markdown("#### " + doc["title"])
            else:
                st.markdown("#### " + f"Document #{index}")

            st.markdown(doc["bullets"])

        elif status == DocStatus.TEXT:
            st.markdown("#### " + f"Document #{index}")
            st.write(doc)

        elif status == DocStatus.ERROR:
            st.sidebar.write(f"Document {index} error")
            # TODO Sam - replace space, so it's a valid link
            # st.markdown(
            #     f"[link](file://data/documents/books/summaries/{book_folder}/summary_{index}.error.txt)"
            # )

        elif status == DocStatus.MISSING:
            st.sidebar.write(f"Document {index} missing")

    st.markdown("-----")
    st.markdown("## Full Summary")
    for index, (status, doc) in enumerate(documents):
        if status == DocStatus.DICT and doc["relevant"]:
            if doc["title"] is not None:
                st.markdown("### " + doc["title"])
            else:
                st.markdown("### " + f"Document #{index}")

            st.write(doc["comprehensive"])

        elif status == DocStatus.TEXT:
            st.markdown("### " + f"Document #{index}")
            st.write(doc)


def authors_to_string(authors):
    return ", ".join(
        list(
            map(
                lambda author: f"{author['name']} ({author['authorship_type']})",
                authors,
            )
        )
    )


def pick_book():
    st.sidebar.title("Pick a book")
    selected_book = None
    for book_folder in os.listdir(summaries_folder):
        if os.path.isdir(os.path.join(summaries_folder, book_folder)):
            clicked = st.sidebar.button(book_folder)
            if clicked:
                selected_book = book_folder

    render(selected_book)


def st_link(text, href=None, sidebar=False):
    if href is None:
        href = text

    destination = st if not sidebar else st.sidebar
    destination.markdown(f"[{text}]({href})")


if __name__ == "__main__":
    pick_book()
