"""
Basic streamlit application to demonstrate retrieval augmented generative (RAG) pipelines.
"""

import streamlit as st
import requests


@st.cache_data
def query_llm(query: str):
    """
    Submits a query to the RAG API and return the result.
    """
    print(f'Query api with "{query}"')
    response = requests.get(
        url="http://127.0.0.1:8000/query", params={"query_string": query}
    )
    json_response = response.json()
    print(json_response)
    return json_response["results"]["llm"]["replies"][0]


def main() -> None:
    """
    Main method that creates the streamlit application with a basic chat prompt.
    Note although the application is presented as a chat view,
    the llm is only provided with the last message as a prompt and so is not aware
    of the chat history.
    """
    st.title("Retrieval Augmented Generation (RAG)")

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "llm", "content": "Ask a question."}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input(placeholder="Enter a question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] != "llm":
        with st.chat_message("llm"):
            with st.spinner("Thinking..."):
                response = query_llm(prompt)
                st.write(response)
                message = {"role": "llm", "content": response}
                st.session_state.messages.append(message)


if __name__ == "__main__":
    main()
