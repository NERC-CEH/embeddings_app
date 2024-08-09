"""
Basic streamlit application to demonstrate retrieval augmented generative
(RAG) pipelines.
"""

import logging

import pandas as pd
import streamlit as st
import yaml

from rag.wrappers import RagPipelineWrapper

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
USER_AVATAR = "🧑‍💻"
LLM_AVATAR = "🦖"

pipeline_file = f"{config["pipelines-dir"]}/{config["rag-demo"]["pipeline"]}"
chroma_path = config["vector-db"]["path"]
collection = config["vector-db"]["collection"]
prompt = config["rag-demo"]["prompt"]
rag_pipe = RagPipelineWrapper(
    pipeline_file,
    chroma_path=chroma_path,
    collection=collection,
    prompt=prompt,
)
example_prompts = config["rag-demo"]["examples"]


@st.cache_data
def query(query: str) -> tuple[str, pd.DataFrame]:
    return rag_pipe.query(query)


def setup_css() -> None:
    """
    Modifies css for primary button types to display as textual links.
    """
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


def main() -> None:
    """
    Main method that creates the streamlit application with a basic chat
    prompt.
    Note although the application is presented as a chat view, the llm is
    only provided with the last message as a prompt and so is not aware of
    the chat history.
    """

    setup_css()

    st.title("EIDC RAG Interface")
    st.logo("docs/img/ceh_logo.png")

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {
                "role": "llm",
                "content": "Please ask a question.",
                "avatar": LLM_AVATAR,
            }
        ]

    with st.sidebar:
        st.sidebar.title("readme")
        st.sidebar.markdown(
            (
                "Welcome to the UKCEH RAG pipeline demo. This streamlit app "
                "provides access to a retrieval augemnted generative pipeline "
                "for querying metadata in the EIDC catalogue."
            )
        )
        st.sidebar.markdown(
            (
                "The prompt will attempt to answer any question you pose to "
                "it based on the data that is available in the EIDC metadata "
                "descriptions. Try it yourself, or click an example query "
                "below."
            )
        )
        st.sidebar.subheader("Examples")
        for example in example_prompts:
            if st.button(example, type="primary"):
                st.session_state.messages.append(
                    {"role": "user", "content": example, "avatar": USER_AVATAR}
                )

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    if prompt := st.chat_input(placeholder="Enter a question"):
        st.session_state.messages.append(
            {"role": "user", "content": prompt, "avatar": USER_AVATAR}
        )
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] != "llm":
        with st.chat_message("llm", avatar=LLM_AVATAR):
            with st.spinner("Thinking..."):
                answer, scores = query(
                    st.session_state.messages[-1]["content"]
                )
                st.write(answer)
                message = {
                    "role": "llm",
                    "content": answer,
                    "avatar": LLM_AVATAR,
                }
                st.session_state.messages.append(message)
                st.dataframe(scores, hide_index=True)


if __name__ == "__main__":
    main()
