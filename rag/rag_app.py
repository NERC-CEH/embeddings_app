"""
Basic streamlit application to demonstrate retrieval augmented generative (RAG) pipelines.
"""

import logging
import requests
import streamlit as st
import pandas as pd
from haystack import Pipeline


logging.getLogger().setLevel(logging.INFO)
USER_AVATAR = '🧑‍💻'
LLM_AVATAR = '🦖'

def stream_callback(chunk):
    """
    Basic callback for streaming responses from an llm or generator.
    """
    print(chunk.content, end="", flush=True)


def load_rag_pipeline(file):
    """
    Loads a pipeline for haystack from a yaml file.
    """
    logging.info(f"Loading {file} as RAG pipeline source.")
    with open(file) as f:
        return Pipeline.loads(f.read())
    

file = "llama3-rag-pipe.yml"
pipeline = load_rag_pipeline(file)


def local_query_llm(query:str):
    results = pipeline.run(
        {
            "retriever": {"query": query},
            "prompt_builder": {"query": query},
            "answer_builder": {"query": query},
        }
    )
    return extract_answer_and_datasets(results)


def extract_answer_and_datasets(response):
    answer = response["answer_builder"]["answers"][0]
    answer_data = answer.data
    docs = [doc.meta['title'] for doc in answer.documents]
    scores = [doc.score for doc in answer.documents]
    df = pd.DataFrame({'dataset': docs, 'score': scores})
    df.sort_values('score', inplace=True, ascending=False)
    return answer_data, df


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
        return extract_answer_and_datasets(json_response)
    except:
        return 'Failed to get response. Check API is running.', None


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

    st.title("EIDC RAG Interface")

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "llm", "content": "Please ask a question.", "avatar": LLM_AVATAR}]

    with st.sidebar:
        st.sidebar.title('readme')
        st.sidebar.markdown('Welcome to the UKCEH RAG pipeline demo. This streamlit app provides access to a retrieval augemnted generative pipeline for querying metadata in the EIDC catalogue.')
        st.sidebar.markdown('The prompt will attempt to answer any question you pose to it based on the data that is available in the EIDC metadata descriptions. Try it yourself, or click an example query below.')
        st.sidebar.subheader('Examples')
        for example in example_prompts:
            if st.button(example, type='primary'):
                st.session_state.messages.append({"role": "user", "content": example, "avatar": USER_AVATAR})

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message['avatar']):
            st.write(message["content"])

    if prompt := st.chat_input(placeholder="Enter a question"):
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": USER_AVATAR})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] != "llm":
        with st.chat_message("llm", avatar=LLM_AVATAR):
            with st.spinner("Thinking..."):
                answer, scores = local_query_llm(st.session_state.messages[-1]["content"])
                st.write(answer)
                message = {"role": "llm", "content": answer, "avatar": LLM_AVATAR}
                st.session_state.messages.append(message)
                st.dataframe(scores, hide_index=True)


if __name__ == "__main__":
    main()
