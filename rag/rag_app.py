"""
Basic streamlit application to demonstrate retrieval augmented generative (RAG) pipelines.
"""

import logging
import requests
import streamlit as st


logging.getLogger().setLevel(logging.INFO)


@st.cache_data
def query_llm(query: str):
    """
    Submits a query to the RAG API and return the result.
    """
    logging.info(f'Querying api with "{query}"')
    try:
        response = requests.get(
            url="http://127.0.0.1:8000/query", params={"query_string": query}
        )
        json_response = response.json()
        logging.info(json_response)
        return json_response["results"]["llm"]["replies"][0]
    except:
        logging.error('Failed to contact API.')
        return 'Problem contacting server. Please check API is running.'


def main() -> None:
    """
    Main method that creates the streamlit application with a basic chat prompt.
    Note although the application is presented as a chat view,
    the llm is only provided with the last message as a prompt and so is not aware
    of the chat history.
    """
    # Example prompts from the initiall LLM scoping work conducted for the data labs enhancement project.
    example_prompts = ["Who collected the land cover map data?", 
                        "Where is the wettest soil in the UK?", 
                        "Where is water quality worst for England?", 
                        "Where are bird populations declining in the UK?", 
                        "Where in the UK are bumblebees most at risk from neonicotinoids?", 
                        "Which county in the UK has the most rivers?"]

    # Modifies css for primary button types to display as textual links.
    st.markdown(
        """
        <style>
        button[kind="primary"] {
            background: none!important;
            border: none;
            padding: 0!important;
            color: #0d68c9 !important;
            text-decoration: none;
            cursor: pointer;
            border: none !important;
            text-align: left !important;
        }
        button[kind="primary"]:hover {
            text-decoration: none;
            color: #4887cb !important;
        }
        button[kind="primary"]:focus {
            outline: none !important;
            box-shadow: none !important;
            color: #92278f !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Retrieval Augmented Generation (RAG)")

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "llm", "content": "Please ask a question."}]

    with st.sidebar:
        st.sidebar.title('readme')
        st.sidebar.markdown('Welcome to the UKCEH RAG pipeline demo. This streamlit app provides access to a retrieval augemnted generative pipeline for querying metadata in the EIDC catalogue.')
        st.sidebar.markdown('The prompt will attempt to answer any question you pose to it based on the data that is available in the EIDC metadata descriptions. Try it yourself, or click an example query below.')
        st.sidebar.subheader('Examples')
        for example in example_prompts:
            if st.button(example, type='primary'):
                st.session_state.messages.append({"role": "user", "content": example})

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
                response = query_llm(st.session_state.messages[-1]["content"])
                st.write(response)
                message = {"role": "llm", "content": response}
                st.session_state.messages.append(message)


if __name__ == "__main__":
    main()
