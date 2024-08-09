#!/usr/bin/env python
from ingestion.wrappers import IndexPipelineWrapper
import logging
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    with open("config.yml", "r") as config_file:
        config = yaml.safe_load(config_file)

    pipeline_file = (
        f"{config['pipelines-dir']}/{config['ingestion']['pipeline']}"
    )
    chroma_path = config["vector-db"]["path"]
    collection = config["vector-db"]["collection"]
    metadata_fields = config["ingestion"]["metadata"]

    logger.info(f"Loading indexing pipeline {pipeline_file}")
    index_pipe = IndexPipelineWrapper(
        pipeline_file,
        chroma_path=chroma_path,
        collection=collection,
    )

    logger.info(
        f'Retrieving data and indexing... [chroma_path="{chroma_path}", collection="{collection}", metadata_field={metadata_fields}]'
    )
    index_pipe.index(metadata_fields=metadata_fields)
