import asyncio
import math
import os
import time
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.callbacks import get_openai_callback
from langchain_community.vectorstores import Milvus
from langchain_core.documents import Document

import ai_researcher.data.db as db
from ai_researcher.bin.streamlit_main import sidebar_menu
from ai_researcher.openai_models import embeddings, embeddings_rate_limiter
from ai_researcher.utils import paths
from ai_researcher.utils.common_utils import (
    authors_to_string,
    format_time,
    read_json,
    sanitize_id,
)

load_dotenv()


def main():
    st.title("Embed Document")
    sidebar_menu()

    st.write("Previously embedded:")
    st.write(
        "\n".join(
            [f"- {embedding_id}" for embedding_id in db.get_all_embedding_ids()]
        )
    )
    st.divider()

    selected_book = book_selector()

    if selected_book is not None:
        st.subheader("RAG settings")

        metadata = read_json(
            os.path.join(paths.splits_raw, selected_book, "metadata.json")
        )

        book_folder = os.path.join(paths.splits_raw, selected_book)
        documents = read_documents(book_folder, metadata["items_length"])

        embedding_id = st.text_input(
            "Embedding ID", value=sanitize_id(metadata["title"])
        )

        chunk_size = st.number_input(
            "Chunk size",
            value=4000,
            min_value=1,
        )
        chunk_overlap = st.number_input(
            "Chunk overlap", value=200, min_value=1, max_value=chunk_size
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            add_start_index=True,
        )
        splits = text_splitter.split_documents(documents)

        preview_splits(splits)

        asyncio.run(embed_book(chunk_size, chunk_overlap, splits, embedding_id))


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


def preview_splits(splits):
    st.write("Total amount of splits: " + str(len(splits)))
    preview_enabled = st.toggle("Preview text-splitting?", False)
    preview_short_enabled = st.toggle(
        "Short preview (use if the other freezes)", False
    )

    if preview_enabled or preview_short_enabled:
        colors = ["red", "green", "orange", "blue", "violet"]

        def find_overlap(doc1, doc2):
            overlap = 0
            for i in range(1, min(len(doc1), len(doc2))):
                if doc1[-i:] == doc2[:i]:
                    overlap = i

            if overlap > 0:
                return doc1[:-overlap], doc1[-overlap:], doc2[overlap:]
            else:
                return doc1, "", doc2

        final_str = ""
        doc1 = splits[0].page_content
        for i in range(1, len(splits)):
            doc1_clean, overlap, doc2_half_clean = find_overlap(
                doc1, splits[i].page_content
            )
            doc1 = doc2_half_clean
            final_str += f":{colors[(i % len(colors))]}[{doc1_clean}]<ins>{overlap}</ins>"
        final_str += doc1

        start_short = math.ceil(len(final_str) / 3)
        end_short = min(math.ceil(len(final_str) * 2 / 3), start_short + 50000)

        st.markdown(
            (
                final_str[start_short:end_short]
                if preview_short_enabled
                else final_str
            ),
            unsafe_allow_html=True,
        )


async def embed_book(
    chunk_size,
    chunk_overlap,
    splits,
    embedding_id,
):
    started = st.button("Start")
    st.warning("This will take a lot of time (a few minutes)!")

    if started:
        progress_bar = st.progress(0)
        progress_text = st.text("0")
        st.write("Embedding documents...")

        vectorstore = Milvus(
            collection_name=os.getenv("MILVUS_COLLECTION"),
            embedding_function=embeddings,
            auto_id=False,
        )
        embedding_time = datetime.now()

        with get_openai_callback() as cb:
            completed_counter = {
                "count": 0
            }  # Using a dict for mutable reference that can be updated across coroutines
            lock = asyncio.Lock()

            tasks = [
                embed_rate_limited(
                    i,
                    embedding_id,
                    embedding_time,
                    splits,
                    vectorstore,
                    completed_counter,
                    lock,
                    progress_bar,
                    progress_text,
                )
                for i, _ in enumerate(splits)
            ]

            await asyncio.gather(*tasks)

            db.add_embedding(
                embedding_id,
                embedding_time,
                map_metadata_for_sqlite(chunk_size, chunk_overlap, len(splits)),
            )

            st.write("Done!")
            progress_bar.progress(1.0)
            st.write(
                f"Total Embedding Time = {format_time( time.time() - embedding_time.timestamp())}"
            )

            st.divider()
            st.write("**API Usage:**")
            st.text(cb)


async def embed_rate_limited(
    i,
    embedding_id,
    embedding_time,
    splits,
    vectorstore,
    completed_counter,
    lock,
    progress_bar,
    progress_text,
):
    async with embeddings_rate_limiter:
        try:
            split = splits[i]
            await vectorstore.aadd_texts(
                texts=[split.page_content],
                metadatas=[
                    map_metadata_for_milvus(
                        split.metadata, embedding_id, embedding_time
                    )
                ],
                ids=[
                    # embedding_id _ chapter_index _ split_index, e.g. breath_2_3
                    f"{embedding_id}_{split.metadata['item_position']}_{i}"
                ],
            )
            async with lock:
                completed_counter["count"] += 1
                progress = completed_counter["count"] / len(splits)
                progress_bar.progress(progress)
                progress_text.text(
                    f"{completed_counter['count']} / {len(splits)}"
                )

        except Exception as e:
            st.write(f":red[Split #{i}: Failed!]")
            st.error(e)


def map_metadata_for_milvus(document_metadata, embedding_id, embedding_time):

    # TODO schema for Metadata:
    # = WEB =
    # url
    # search_id - guid
    # page title (bud zo search alebo z <head>)
    #

    # = kniha =
    # book_title
    # authors [name, authorship_type]
    # source - filename.epub
    # source_type - epub, mobi, pdf
    # item_id - chapter id
    # item_position - chapter order
    # total_items - total chapters
    # start_index - chunk splitu
    # \

    return {
        **document_metadata,
        "embedding_id": embedding_id,
        "embedding_time": embedding_time.isoformat(),
        "authors": authors_to_string(document_metadata["authors"]),
    }


def map_metadata_for_sqlite(chunk_size, chunk_overlap, total_chunks):
    return {
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "total_chunks": total_chunks,
    }


if __name__ == "__main__":
    main()
