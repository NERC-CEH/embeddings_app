#!/bin/bash
/bin/ollama serve &
pid=$!
sleep 5
echo "Pulling model[llama3.1]..."
ollama pull llama3.1
echo "Finished pulling model"
wait $pid

# Script based upon https://stackoverflow.com/questions/78500319/how-to-pull-model-automatically-with-container-creation/78501628#78501628