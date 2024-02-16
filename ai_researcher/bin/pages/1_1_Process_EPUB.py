import os
import tempfile

import streamlit as st

from ai_researcher import paths
from ai_researcher.document_loaders.epub_loader import EPubLoader
from ai_researcher.utils import (
    sanitize_filename,
    dump_json,
)


def process_book(book_path, original_file_name):
    progress_bar = st.progress(0)

    loader = EPubLoader(book_path)
    documents = loader.load()

    book_folder = sanitize_filename(loader.title)
    data_folder = os.path.join(paths.splits_raw, book_folder)

    dump_json(
        {
            "title": loader.title,
            "authors": loader.authors,
            "items_length": loader.items_length,
            "file_name": original_file_name,
        },
        os.path.join(data_folder, "metadata.json"),
    )
    progress_bar.progress(1 / (len(documents) + 1))

    for i, doc in enumerate(documents):
        destination = os.path.join(data_folder, f"doc_{i}.json")
        dump_json(
            {"page_content": doc.page_content, "metadata": doc.metadata},
            destination,
        )
        progress_bar.progress((i + 2) / (len(documents) + 1))

    st.write("Done!")
    st.write(
        f"Chapters saved to: `{os.path.abspath(data_folder)}`",
    )

    return book_folder


if __name__ == "__main__":
    st.title("Process a new book")
    uploaded_file = st.file_uploader("Select EPUB file", type=["epub"])

    if uploaded_file is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            temp_file.write(uploaded_file.getvalue())
            temp_file.close()
            process_book(temp_file.name, uploaded_file.name)
        finally:
            os.remove(temp_file.name)