import streamlit as st


def sidebar_menu():
    st.sidebar.header("Load")
    st.sidebar.page_link("pages/load_epub.py", label="EPUB")

    st.sidebar.header("Transform")
    st.sidebar.page_link("pages/transform_summarize.py", label="Summarize")
    st.sidebar.page_link("pages/transform_embed.py", label="Embed")

    st.sidebar.header("View")
    st.sidebar.page_link("pages/view_summary.py", label="Summary")
    st.sidebar.page_link("pages/view_retrieve.py", label="Retrieval")
    st.sidebar.page_link("pages/view_rag.py", label="RAG")


if __name__ == "__main__":
    st.title("AI Researcher UI Prototypes")
    st.write("Select what you want to do in the sidebar.")
    sidebar_menu()
