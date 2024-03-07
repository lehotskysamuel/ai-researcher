import streamlit as st
from langchain_community.vectorstores import Milvus

from ai_researcher.bin.streamlit_main import sidebar_menu
from ai_researcher.openai_models import embeddings


def main():
    st.title("Retrieve")
    sidebar_menu()

    query = st.text_input("Query")

    if query:
        retrieve(query)
    else:
        st.write("null")


def retrieve(query):
    vectorstore = Milvus(
        embedding_function=embeddings,
        auto_id=False,
    )

    retrieved_docs = vectorstore.similarity_search_with_score(query, 1000)
    # retriever = vectorstore.as_retriever()
    # retriever = db.as_retriever(search_kwargs={"k": 1})
    # vectorstore.as_retriever(
    #     search_kwargs={"expr": 'namespace == "ankush"'}
    # )
    # retrieved_docs = retriever.invoke("How does Mortarion look like?")
    st.write(retrieved_docs[3][0].page_content)

    st.write(
        (
            f"Score: {str(score)}",
            f"Primary Key: {doc.metadata['pk']}",
            f"Chapter: {doc.metadata['item_position']}",
            f"Start: {doc.metadata['start_index']}",
        )
        for (doc, score) in retrieved_docs
    )

    ### Search types:
    # vectorstore.similarity_search - klasika
    # vectorstore.similarity_search_with_score - vrati mi aj skore
    # vectorstore.similarity_search_by_vector - sam si spocitam embedding z query (aby som vedel vektor - ked ho napr. chcem dat do grafu)
    # vectorstore.similarity_search_by_vector_with_score - vlastny vektor a vrati skore
    # vectorstore.max_marginal_relevance_search - mmr - ak mam prilis podobne chunky (vela duplikatov atd) - vrati top vysledky, ale ignoruje tie duplikaty, berie do uvahy diverzitu - odstranovanie duplikatov je na urovni kodu; na urovni DB je len zakaldny similarity search


# TODO: MultiQueryRetrieve, MultiVectorRetriever
# retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
# https://python.langchain.com/docs/modules/data_connection/retrievers/self_query - filtrovanie podla metadat


if __name__ == "__main__":
    main()
