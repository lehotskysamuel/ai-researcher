import json
import os

import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from langchain_community.vectorstores import Milvus
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables import RunnablePassthrough

import ai_researcher.data.db as db
from ai_researcher.bin.streamlit_main import sidebar_menu
from ai_researcher.openai_models import embeddings, gpt4

load_dotenv()


def main():
    # TODO ako riesit kontext a last message history pri RAG? Kolko poslednych sprav zobrazit? Pozriet langchain docs (ten chat a github repo)
    # TODO - asi to riesia takto https://python.langchain.com/docs/use_cases/question_answering/chat_history

    st.title("RAG Chatbot")
    sidebar_menu()

    selected_embeddings = embedding_selector()

    history = StreamlitChatMessageHistory(key="chat_messages")
    for msg in history.messages:
        st.chat_message(map_message_type(msg.type)).write(msg.content)

    if question := st.chat_input("Say something"):
        st.chat_message("user").write(question)
        get_response(question, selected_embeddings, history)

    reset_button(history)


def map_message_type(msg_type):
    if msg_type == "AIMessageChunk":
        return "ai"
    else:
        return msg_type


def reset_button(history):
    if len(history.messages) > 1:
        if reset_clicked := st.button("Reset Conversation"):
            history.clear()
            st.rerun()


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


def get_response(question, embedding_ids, history):
    retrieved_docs = retrieve_relevant_docs(question, embedding_ids)
    context = "\n---\n".join(doc.page_content for doc in retrieved_docs)

    prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                f"""You are an assistant and your task is to answer questions.
                Use the following pieces of context to answer the question.
                Always answer based on the context provided.
                If the context doesn't include information necessary to answer the question,
                just say there is not enough information to answer the question.
                
                Question: {{question}}
                
                Context:
                ======
                {context}
                ======
                 
                Your Answer: """,
            ),
            # MessagesPlaceholder(variable_name="history"),
            # HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )

    base_chain = {"question": RunnablePassthrough()} | prompt_template | gpt4

    response = base_chain.stream(question)

    # chain_with_history = RunnableWithMessageHistory(
    #     base_chain,
    #     lambda session_id: history,  # Always return the same instance and ignore session_id
    #     input_messages_key="question",
    #     history_messages_key="history",
    # )
    # config = {"configurable": {"session_id": "any"}}
    # response = chain_with_history.stream({"question": question}, config)

    st.chat_message("ai").write_stream(response)


def retrieve_relevant_docs(question, embedding_ids):
    vectorstore = Milvus(
        collection_name=os.getenv("MILVUS_COLLECTION"),
        embedding_function=embeddings,
        auto_id=False,
    )

    k_results = 10
    retrieved_docs = vectorstore.similarity_search(
        question, k_results, expr=f"embedding_id in {json.dumps(embedding_ids)}"
    )
    return retrieved_docs


if __name__ == "__main__":
    main()
