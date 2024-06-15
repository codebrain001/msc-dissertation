from llama_index.core.llama_pack import download_llama_pack
import os
import openai

open_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = open_api_key

# download and install dependencies
RAFTDatasetPack = download_llama_pack("RAFTDatasetPack", "./raft_dataset_pack")

raft_dataset = RAFTDatasetPack('/Users/codebrain/Desktop/PROM02/msc-dissertation/data/uk_anthem.pdf')

dataset = raft_dataset.run()

print('Dataset content:')
print(dataset)
print('done')