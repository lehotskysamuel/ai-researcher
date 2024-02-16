import os
import time

import streamlit as st
from langchain_community.callbacks import get_openai_callback
from langchain_core.documents import Document
from langchain_core.exceptions import OutputParserException
from streamlit_modal import Modal

from ai_researcher import paths
from ai_researcher.summarizers.prose_summarizer import ProseSummarizer
from ai_researcher.utils import (
    read_json,
    read_raw,
    dump_raw,
    dump_json,
    copy_file,
)


def main():
    st.title("Summarize book")

    selected_book = book_selector()

    if selected_book is not None:
        st.subheader("Summarization settings")

        metadata = read_json(
            os.path.join(paths.splits_raw, selected_book, "metadata.json")
        )

        start_split, end_split = split_selectors(metadata["items_length"])

        selected_prompt = prompt_selector()

        if selected_prompt is not None:
            started = st.button("Start")
            st.warning("This will take a lot of time (a few minutes)!")

            if started:
                summarize(
                    selected_book,
                    metadata,
                    selected_prompt,
                    start_split,
                    end_split,
                )


def book_selector():
    book_folders = [
        book_folder
        for book_folder in os.listdir(paths.splits_raw)
        if os.path.isdir(os.path.join(paths.splits_raw, book_folder))
    ]
    selected_book = st.selectbox(
        "Which book would you like to summarize?",
        book_folders,
        index=None,
        placeholder="Select a book...",
    )
    return selected_book


def split_selectors(items_amount):
    min_split = 0
    max_split = items_amount - 1

    start_split = st.number_input(
        "Start with Split: ",
        value=min_split,
        min_value=min_split,
        max_value=max_split,
    )
    end_split = st.number_input(
        "End with Split: ",
        value=max_split,
        min_value=min_split,
        max_value=max_split,
    )

    return start_split, end_split


def prompt_selector():
    prompts = [
        prompt
        for prompt in os.listdir(paths.prompts)
        if os.path.isfile(os.path.join(paths.prompts, prompt))
    ]
    selected_prompt = st.selectbox(
        "Which prompt would you like to use for summarization?",
        prompts,
        index=None,
        placeholder="Select a prompt...",
    )

    if selected_prompt is not None:
        modal = Modal(
            "Prompt Preview",
            key="prompt-preview-modal",
        )
        open_modal = st.button("Preview prompt")
        if open_modal:
            modal.open()
        if modal.is_open():
            with modal.container():
                st.text(read_raw(os.path.join(paths.prompts, selected_prompt)))

    return selected_prompt


def summarize(selected_book, metadata, selected_prompt, start_split, end_split):
    book_folder = os.path.join(paths.splits_raw, selected_book)

    documents = read_documents(book_folder, start_split, end_split)

    copy_file(
        os.path.join(book_folder, "metadata.json"),
        os.path.join(paths.summary, selected_book, "metadata.json"),
    )

    progress_bar = st.progress(0)

    time.sleep(1)
    with get_openai_callback() as cb:
        for i in range(start_split, end_split + 1):
            doc = documents[i]
            st.write(f"Split #{i}: In Progress...")

            summarizer = ProseSummarizer(doc)

            time.sleep(1)
            continue

            try:
                summary = summarizer.summarize()
                dump_json(
                    summary,
                    os.path.join(
                        paths.summary, selected_book, f"summary_{i}.json"
                    ),
                )
                st.write(":green[Split #{i}: Successful!]")
            except OutputParserException as e:
                dump_raw(
                    e.llm_output,
                    os.path.join(
                        paths.summary,
                        selected_book,
                        f"summary_{i}.fallback.json",
                    ),
                )
                st.write(
                    ":orange[Split #{i}: finished with parser exception, falling back to text mode.]"
                )
            except Exception as e:
                try:
                    dump_raw(
                        str(e),
                        os.path.join(
                            paths.summary,
                            selected_book,
                            f"summary_{i}.error.json",
                        ),
                    )
                    st.write(":red[Split #{i}: Failed, error saved!]")
                    st.error(e)
                except e2:
                    st.write(":red[Split #{i}: Failed, error lost!]")
                    st.error(e)
                    st.error(e2)
                    pass

            progress_bar.progress(
                (i - start_split + 1) / (end_split - start_split + 1)
            )

        st.write("Done!")
        st.write("<hr>", unsafe_allow_html=True)
        st.write("**API Usage:**")
        st.text(cb)


def read_documents(book_folder, start_split, end_split):
    documents = []

    for i in range(start_split, end_split + 1):
        doc_path = f"{book_folder}/doc_{i}.json"
        doc_json = read_json(doc_path)
        documents.append(
            Document(
                page_content=doc_json["page_content"],
                metadata=doc_json["metadata"],
            )
        )

    return documents


if __name__ == "__main__":
    main()
