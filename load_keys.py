import os
import openai

def load_OpenAI_key():
    with open("D:/Coding/key.txt", "r") as fin:
        os.environ["OPENAI_API_KEY"] = fin.readline()
        openai.api_key = os.environ["OPENAI_API_KEY"]

def load_weather_key():
    os.environ["WEATHER_API_KEYS"] = "ea46fd88ecf64962a0830641230307"
