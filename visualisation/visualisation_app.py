"""
Streamlit application to view EIDC datasets using their document embeddings
"""

from ast import literal_eval
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import chromadb
import pandas as pd

cdb = chromadb.HttpClient(host="localhost", port=8000)


@st.cache_data
def get_embeddings(collection_name: str) -> pd.DataFrame:
    """
    Retrieve document embeddings from chroma database.
    """
    collection = cdb.get_collection(collection_name)
    result = collection.get(include=["metadatas"])
    reduced_embeddings = [
        literal_eval(metadata["umap_reduced"]) for metadata in result["metadatas"]
    ]
    df = pd.DataFrame(reduced_embeddings, columns=["x", "y"])
    df["title"] = [metadata["title"] for metadata in result["metadatas"]]
    df["description"] = [metadata["description"] for metadata in result["metadatas"]]
    df["lineage"] = [metadata["lineage"] for metadata in result["metadatas"]]
    df["topic"] = [metadata["topic_keywords"] for metadata in result["metadatas"]]
    df["topic_number"] = [metadata["topic_number"] for metadata in result["metadatas"]]
    df["doc_id"] = result["ids"]
    df["short_title"] = [
        title[:50] + "..." if len(title) > 15 else title
        for title in df["title"].to_list()
    ]
    return df


def create_figure(df: pd.DataFrame) -> go.Figure:
    """
    Creates scatter plot based on handed data frame
    """
    color_dict = {i: px.colors.qualitative.Alphabet[i] for i in range(0, 20)}
    color_dict[-1] = "#ABABAB"
    topic_color = df["topic_number"].map(color_dict)
    fig = go.Figure(
        data=go.Scatter(
            x=df["x"],
            y=df["y"],
            mode="markers",
            marker_color=topic_color,
            customdata=df["doc_id"],
            text=df["short_title"],
            hovertemplate="<b>%{text}</b>",
        )
    )
    fig.update_layout(height=600)
    return fig


def update_text(title: str, desc: str, topic: str, col) -> None:
    """
    Updates the texts in the passed column with details of the currently selected dataset.
    """
    with col:
        st.markdown(f"**{title}**")
        st.markdown(f"*{topic}*")
        st.markdown(desc)


def extract_details(df: pd.DataFrame, doc_id: str) -> str | str | str:
    """
    Extract title, description and topic details from a dataframe based on the an id.
    """
    selection = df[df["doc_id"] == doc_id]
    title = selection["title"].iloc[0]
    desc = selection["description"].iloc[0]
    topic = selection["topic"].iloc[0]
    return title, desc, topic


def main() -> None:
    """
    Main method that sets up the streamlit app and builds the visualisation.
    """
    st.set_page_config(layout="wide", page_title="EIDC Dataset Embeddings")
    st.title("EIDC Dataset Embeddings")
    col1, col2 = st.columns([3, 1])

    df = get_embeddings("eidc_datasets")
    fig = create_figure(df)

    event = col1.plotly_chart(
        fig, key="embeddings", on_select="rerun", selection_mode="points"
    )
    if len(event["selection"]["points"]) > 0:
        point = event.selection.points[0]
        doc_id = point["customdata"]
        title, desc, topic = extract_details(df, doc_id)
        update_text(title, desc, topic, col2)


if __name__ == "__main__":
    main()