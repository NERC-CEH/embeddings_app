from datasets import load_dataset
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from ragas import evaluate
from ragas.metrics import (
    context_precision,
)

if __name__ == "__main__":
    qa = load_dataset(
        "explodinggradients/amnesty_qa", "english_v2", trust_remote_code=True
    )
    subset = qa["eval"].select(range(2))
    print(subset.to_pandas())
    llm = ChatOllama(model="llama3")
    embeddings = OllamaEmbeddings(model="llama3")
    response = llm.invoke("Tell me a joke")
    result = evaluate(
        subset, metrics=[context_precision], llm=llm, embeddings=embeddings
    )
