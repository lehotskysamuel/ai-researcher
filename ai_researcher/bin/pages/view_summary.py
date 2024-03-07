import os
from enum import Enum

import streamlit as st
from streamlit_modal import Modal

from ai_researcher import paths
from ai_researcher.bin.streamlit_main import sidebar_menu
from ai_researcher.utils import authors_to_string, is_blank, read_json, read_raw


class DocStatus(Enum):
    DICT = "DICT"
    TEXT = "TEXT"
    ERROR = "ERROR"
    MISSING = "MISSING"


def render_summary(book_folder):
    try:
        metadata = read_json(os.path.join(book_folder, "metadata.json"))
    except IOError as e:
        st.error("Metadata corrupted: " + str(e))
        return

    st.title(metadata["title"])
    authors = authors_to_string(metadata["authors"])
    st.write("Authors: ", authors)

    modal = Modal(
        "Prompt Used",
        key="prompt-modal",
    )
    open_modal = st.button("See prompt used to generate this summary")
    if open_modal:
        modal.open()
    if modal.is_open():
        with modal.container():
            st.text(read_raw(os.path.join(book_folder, "prompt.txt")))

    documents = load_documents(book_folder, metadata["items_length"])

    st.markdown("## Short Summary")
    for index, (status, doc) in enumerate(documents):
        if status == DocStatus.DICT and doc["relevant"]:
            if not is_blank(doc["title"]):
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
            st.write(f"Document {index} missing")

    st.markdown("-----")
    st.markdown("## Full Summary")
    for index, (status, doc) in enumerate(documents):
        if status == DocStatus.DICT and doc["relevant"]:
            if not is_blank(doc["title"]):
                st.markdown("### " + doc["title"])
            else:
                st.markdown("### " + f"Document #{index}")

            st.write(doc["comprehensive"])

        elif status == DocStatus.TEXT:
            st.markdown("### " + f"Document #{index}")
            st.write(doc)


def load_documents(book_folder, items_length):
    docs = []
    for i in range(items_length):
        try:
            doc = read_json(os.path.join(book_folder, f"summary_{i}.json"))
            docs.append((DocStatus.DICT, doc))
        except FileNotFoundError:
            try:
                doc = read_raw(
                    os.path.join(book_folder, f"summary_{i}.fallback.txt")
                )
                docs.append((DocStatus.TEXT, doc))
            except FileNotFoundError:
                try:
                    doc = read_raw(
                        os.path.join(book_folder, f"summary_{i}.error.txt")
                    )
                    docs.append((DocStatus.ERROR, doc))
                except FileNotFoundError:
                    docs.append((DocStatus.MISSING, None))
    return docs


if __name__ == "__main__":
    st.title("Summary Viewer")
    sidebar_menu()

    book_folders = [
        book_folder
        for book_folder in os.listdir(paths.summary)
        if os.path.isdir(os.path.join(paths.summary, book_folder))
    ]

    selected_book = st.selectbox(
        "Which book summary would you like to view?",
        book_folders,
        index=None,
        placeholder="Select a book...",
    )

    if selected_book is not None:
        st.divider()
        render_summary(os.path.join(paths.summary, selected_book))
