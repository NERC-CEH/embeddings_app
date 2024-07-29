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

![Embeddings Visualisation](/docs/img/viz.png)

# RAG (Retrieval Augmented Generation) App
This application run a retrieval augmented generative pipeline using [Haystack](https://haystack.deepset.ai/), [Chroma](https://www.trychroma.com/), [FastAPI](https://fastapi.tiangolo.com/) and a simple user interface using [Streamlit](https://streamlit.io/).

## Setup
Ensure you have followed the steps listed above to start Chroma and upload the EIDC embeddings data. You can then stop the Chroma server and follow the steps below.

## Ollama
The demo application uses the RAG pipeline defined in `llama3-rag-pipe.yml` which makes use of the `llama3` model via [Ollama](https://ollama.com/). Check the ollama website for most recent setup guide but for brevity you can follow the following basic instructions:

Download and run the ollama installer shell script:
```shell
curl -fsSL https://ollama.com/install.sh | sh
```
Load the llama3 model into ollama and check it runs:
```shell
ollama run llama3
```
> Use `/bye` to exit the ollama shell.
The llama3 model should now be available via the ollama rest API at [http://localhost:11434](http://localhost:11434)

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