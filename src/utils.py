import os
import openai

def load_OpenAI_key(path="../key.txt"):
    with open(path, "r") as fin:
        os.environ["OPENAI_API_KEY"] = fin.readline()
        openai.api_key = os.environ["OPENAI_API_KEY"]