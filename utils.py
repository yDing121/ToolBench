import openai


def get_set_key(path="../key.txt"):
    with open(path, "r") as fin:
        openai.api_key = fin.readline()