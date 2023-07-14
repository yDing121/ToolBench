import json
import os
import sys
from typing import Any, List, Mapping, Optional

import openai
from my_utils.load_keys import load_key
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM


def call_model(prompt, try_times=5):
    """
    Calls the OpenAI model specified by the input arguments and returns the model's response as a OpenAI response
    object.

    Parameters:
        prompt (str): the prompt that will be given to the model.

        try_times (int): the number of attempts at calling the model, after an error is raised but the program is
        not stopped

    Returns:
        completion: the model's response as an OpenAI response object. For what a raw response (as a string) looks like,
        refer to /data-generation/queries/response.txt
    """
    while try_times > 0:
        openai.api_key = os.environ["OPENAI_API_KEY"]
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a user what to consult the assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                max_tokens=1024
            )
            break
        except:
            try_times -= 1
            continue

    if try_times == 0:
        raise RuntimeError("Your LLM service is not available.")

    return str(completion)


def parse_raw(raw_input):
    """
    Extracts the
    """
    output = json.loads(raw_input)["choices"][0]["message"]["content"]
    return output


if __name__ == "__main__":
    load_key("openai")
    res = call_model("Write a brief self introduction")
    print(res)
