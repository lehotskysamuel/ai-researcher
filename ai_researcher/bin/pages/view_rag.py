import json
import os

import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import Milvus

import ai_researcher.data.db as db
from ai_researcher.bin.streamlit_main import sidebar_menu
from ai_researcher.openai_models import embeddings

load_dotenv()


def main():
    # TODO ako riesit kontext a last message history pri RAG? Kolko poslednych sprav zobrazit? Pozriet langchain docs (ten chat a github repo)

    st.title("RAG Chatbot")
    sidebar_menu()

    query = st.text_input("Query")
    selected_embeddings = embedding_selector()

    k_results = st.number_input(
        "Number of results",
        min_value=1,
        value=10,
        step=1,
    )

    if query and len(selected_embeddings) > 0:
        retrieve(query, selected_embeddings, k_results)


def embedding_selector():
    embedding_ids = [
        embedding_id for embedding_id in db.get_all_embedding_ids()
    ]

    selected_embeddings = st.multiselect(
        "What sources would you like to query?",
        embedding_ids,
        placeholder="Select sources...",
    )

    return selected_embeddings


def retrieve(query, embedding_ids, k_results):
    vectorstore = Milvus(
        collection_name=os.getenv("MILVUS_COLLECTION"),
        embedding_function=embeddings,
        auto_id=False,
    )

    retrieved_docs = vectorstore.similarity_search_with_score(
        query, k_results, expr=f"embedding_id in {json.dumps(embedding_ids)}"
    )

    # retriever = MultiQueryRetriever.from_llm(
    #     retriever=vectorstore.as_retriever(
    #         search_kwargs={
    #             "k": k_results, # generates k results per each query, then makes a unique union
    #             "expr": f"embedding_id in {json.dumps(embedding_ids)}",
    #         }
    #     ),
    #     llm=gpt4,
    # )
    # retrieved_docs = retriever.invoke(query)
    # st.write(retrieved_docs)

    for doc, score in retrieved_docs:
        with st.expander(
            f"({format_score(score)}) **{doc.metadata['embedding_id']}**  |  *Position*: {doc.metadata['item_position']}"
        ):
            st.write(doc.page_content)


def format_score(num):
    if num < 100:
        return f"{num * 100:.0f}"
    else:
        return f"{num/10:.1f}k"


if __name__ == "__main__":
    main()
