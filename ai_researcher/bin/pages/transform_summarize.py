import math
import os
from enum import Enum

import streamlit as st
from langchain_community.callbacks import get_openai_callback
from langchain_core.documents import Document
from langchain_core.exceptions import OutputParserException
from streamlit_modal import Modal

from ai_researcher import paths
from ai_researcher.bin.streamlit_main import sidebar_menu
from ai_researcher.summarizers.prose_summarizer import ProseSummarizer
from ai_researcher.utils import (
    copy_file,
    dump_json,
    dump_raw,
    read_json,
    read_raw,
)


class LengthOption(Enum):
    SHORT = "Short"
    NORMAL = "Normal"
    LONG = "Long"


def main():
    st.title("Summarize")
    sidebar_menu()

    selected_book = book_selector()

    if selected_book is not None:
        st.subheader("Summarization settings")

        metadata = read_json(
            os.path.join(paths.splits_raw, selected_book, "metadata.json")
        )

        start_split, end_split = split_selectors(metadata["items_length"])

        selected_length = length_selector()
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
                    selected_length,
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


def length_selector() -> LengthOption:
    length_options = [option for option in LengthOption]
    selected_length = st.selectbox(
        "How long should the summary be?",
        length_options,
        format_func=lambda x: x.value,
        index=1,
        placeholder="Choose length...",
    )

    return selected_length


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
    prompt_text = None

    if selected_prompt is not None:
        prompt_text = read_raw(os.path.join(paths.prompts, selected_prompt))

        modal = Modal(
            "Prompt Preview",
            key="prompt-preview-modal",
        )
        open_modal = st.button("Preview prompt")
        if open_modal:
            modal.open()
        if modal.is_open():
            with modal.container():
                st.text(prompt_text)

    return prompt_text


def summarize(
    selected_book,
    metadata,
    summary_instructions,
    start_split,
    end_split,
    selected_length: LengthOption,
):
    book_folder = os.path.join(paths.splits_raw, selected_book)

    documents = read_documents(book_folder, metadata["items_length"])

    copy_file(
        os.path.join(book_folder, "metadata.json"),
        os.path.join(paths.summary, selected_book, "metadata.json"),
    )

    dump_raw(
        summary_instructions,
        os.path.join(paths.summary, selected_book, "prompt.txt"),
    )

    progress_bar = st.progress(0)

    with get_openai_callback() as cb:
        for i in range(start_split, end_split + 1):
            doc = documents[i]
            st.write(f"Split #{i}: In Progress...")

            summarizer = ProseSummarizer(doc, summary_instructions)

            length_modifier = (
                1650
                if selected_length == LengthOption.SHORT
                else 1100 if selected_length == LengthOption.NORMAL else 550
            )
            paragraphs_target = math.ceil(
                summarizer.model.get_num_tokens(doc.page_content)
                / length_modifier
            )

            try:
                summary = summarizer.summarize(paragraphs_target)
                dump_json(
                    summary,
                    os.path.join(
                        paths.summary, selected_book, f"summary_{i}.json"
                    ),
                )
                st.write(f":green[Split #{i}: Successful!]")
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
                    f":orange[Split #{i}: finished with parser exception, falling back to text mode.]"
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
                    st.write(f":red[Split #{i}: Failed, error saved!]")
                    st.error(e)
                except Exception as e2:
                    st.write(f":red[Split #{i}: Failed, error lost!]")
                    st.error(e)
                    st.error(e2)
                    pass

            progress_bar.progress(
                (i - start_split + 1) / (end_split - start_split + 1)
            )

        st.write("Done!")
        st.divider()
        st.write("**API Usage:**")
        st.text(cb)


def read_documents(book_folder, length):
    documents = []

    for i in range(0, length):
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
