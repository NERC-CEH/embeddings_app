This repository contains a demo for visualising and interacting with datasets in the EIDC based on their metadata descriptions found in the metadata catalogue.

# Requirements
The follow requirments shoud be installed:
- Python 3.12

# Setup
## Install Python Packages
> It is recommended you create a new [python virtual environment](https://docs.python.org/3/library/venv.html) whenever running a python project. e.g. `python -m venv .venv`, `source .venv/bin/activate`

First install required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

# Visualisation App
## Startup Chroma
The [Chroma](https://www.trychroma.com/) database should be started in server mode. This database stores the embeddings used in the demo. To start:
```bash
chroma run --path chroma-data
```
This will start the database server and store the data in `chroma_data`. By default the database should run on port `8000`.

## Upload Data
To upload data to chroma simply run:
```bash
./add_embeddings.py
```
This script assumes you are using a python virtual environemnt and that the data is contained in a file named `eidc_embeddings.csv` which should look like this:

| embeddings | umap_reduced | title | description | lineage | topic_number | topic_keywords |
| ---------- | ------------ | ----- | ----------- | ------- | ------------ | -------------- |
| [-1.77440979e-03, -4.55704965e-02, 5.42910360... | [6.1172633, 6.4104953] | High resolution water quality and flow monitor... | This data set comprises of hourly water qualit... | Water quality and flow data from the Bow Brook... | 1 | ['water samples', 'catchment', 'catchments', '... |
| ...        |              |       |             |         |              |                |
| ...        |              |       |             |         |              |                |


## Run Streamlit
The application runs using [Streamlit](https://streamlit.io/). To start it up use:
```bash
streamlit run visualisation/visualisation_app.py
```

## Connect
The demo should automatically open in you browser when you run streamlit. If it does not, connect using: [http://localhost:8501](http://localhost:8501).

# RAG (Retrieval Augmented Generation) App
This application run a retrieval augmented generative pipeline using [Haystack](https://haystack.deepset.ai/), [Chroma](https://www.trychroma.com/), [FastAPI](https://fastapi.tiangolo.com/) and a simple user interface using [Streamlit](https://streamlit.io/).

## Setup
Ensure you have followed the steps listed above to start Chroma and upload the EIDC embeddings data. You can then stop the Chroma server and follow the steps below.

## Start FastAPI
First start up the RAG API:
```shell
fastapi dev rag/rag_api.py
```
This hosts the haystack pipeline and will access the data in chromadb directly.

## Run Streamlit
To start the streamlit UI:
```shell
streamlit run rag/rag_app.py
```

The user interface should then be available at [http://localhost:8501](http://localhost:8501).