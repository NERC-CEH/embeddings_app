This repository contains a demo for visualising and interacting with datasets in the EIDC based on their metadata descriptions found in the metadata catalogue.

# Requirements
The follow requirments shoud be installed:
- Python 3.12

# Setup
## Install Python Packages
Setup a new [python virtual environment](https://docs.python.org/3/library/venv.html) 
```shell
python -m venv .venv`, `source .venv/bin/activate
```

Install the required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

# Ingestion
To run all the demos you will need to download the metadata from the EIDC catalogue and load it into a Chroma vector database. A convenience pipeline has been written to handle this task. The pipeline is defined in `pipelines/index.yml` and it can be easily run using `load_embeddings.py`:
```shell
./load_embeddings.py
```
> This script assumes you have activated a python `venv` and install the required dependnecies.
This ingestion pipeline will download the metadata avaialble in the EIDC catalgoue, convert and store the metadata in a chroma instance. Setting for defining the file path to the chroma data, the collection to use, and which metadata fields to store is defined in `config.yml`

# Visualisation App
## Run Streamlit
All demos run using [Streamlit](https://streamlit.io/). To start the visualisation demo use:
```bash
python -m streamlit run visualisation/visualisation_app.py
```

## Connect
The demo should automatically open in you browser when you run streamlit. If it does not, connect using: [http://localhost:8501](http://localhost:8501).

![Embeddings Visualisation](/docs/img/viz.png)

# RAG (Retrieval Augmented Generation) App
This application run a retrieval augmented generative pipeline using [Haystack](https://haystack.deepset.ai/), [Chroma](https://www.trychroma.com/), [FastAPI](https://fastapi.tiangolo.com/) and a simple user interface using [Streamlit](https://streamlit.io/). The pipeline is defined in `pipelines/llama3.1-rag-pipe.yml` and can be seen below:
![NER Mapping UI](/docs/img/llama3-rag-pipe.png)

## Ollama
The RAG pipeline makes use of the `llama3.1` model via [Ollama](https://ollama.com/). Check the ollama website for most recent setup guide but for brevity you can follow the following basic instructions:

Download and run the ollama installer shell script:
```shell
curl -fsSL https://ollama.com/install.sh | sh
```
Load the llama3.1 model into ollama and check it runs:
```shell
ollama run llama3.1
```
> Use `/bye` to exit the ollama shell.
The llama3.1 model should now be available via the ollama rest API at [http://localhost:11434](http://localhost:11434)

## Run Streamlit
To start the streamlit UI:
```shell
python -m streamlit run rag/rag_app.py
```

The user interface should then be available at [http://localhost:8501](http://localhost:8501).

![RAG User Interface](/docs/img/rag.png)

# Map App
This application performs basic NER (Named Entity Recognition) on an input query using [Spacy](https://spacy.io/). Any detected geographic place names (GPE) are automatically geocoded using [Nominatim](https://nominatim.org/) through [GeoPy](https://geopy.readthedocs.io/) and then displayed to a map using [Folium](https://python-visualization.github.io/folium). The NER results are also dispayed using [Displacy](https://demos.explosion.ai/displacy).

## Run Streamlit
The application simply runs via streamlit:
```shell
python -m streamlit run map/map_app.py
```
![NER Mapping UI](/docs/img/map_app.png)