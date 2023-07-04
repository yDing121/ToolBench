"""
Loads API keys into the operating environment as environmental variables.
The keys still have to be retrieved from the environment by the programs using them
"""

import os
import json

with open("D:/Coding/keys.json", "r") as fin:
    # print("thing")
    keydata = json.load(fin)
    # print("Openai:\t", keydata["openai"])
    # print(type(keydata))


def load_key(key_short):
    pair = keydata[key_short]
    os.environ[pair["code"]] = pair["key"]
    print(f"Loaded {key_short} API")
    