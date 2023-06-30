# coding=utf-8
# Copyright 2023 The OpenBMB team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json
from tqdm import tqdm
import multiprocessing as mp
import requests
import time
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default="gpt-3.5-turbo", required=False, help='model name')
parser.add_argument('--max_tokens', type=int, default=3072, required=False, help='max tokens')
parser.add_argument('--frequency_penalty', type=float,  default=0, required=False, help='frequency_penalty')
parser.add_argument('--presence_penalty', type=float, required=False, default=0, help='presence_penalty')
parser.add_argument('--best_of', type=int, default=3, required=False, help='best_of')
parser.add_argument('--stop', type=str, default=None, required=False, help='stop')
parser.add_argument('--prompt', type=str, default="You are a user what to consult the assistant.", required=False, help='prompt')
parser.add_argument('--parallel', type=int, default=1, required=False, help='parallel')
parser.add_argument('--total_num', type=int, default=100, required=False, help='total number of queries')
parser.add_argument('--tool_name', type=str, default="stock", required=False, help='tool name')
args = parser.parse_args()

# chatgpt
url = "ChatGPT's calling URL"

headers = {
    "Content-Type": "application/json"
}


def get_payload(prompt):
    payload = {
        "model": args.model,
        "messages": [
            {"role": "system", "content": "You are a user what to consult the assistant."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": args.max_tokens,
        "frequency_penalty": args.frequency_penalty,
        "presence_penalty": args.presence_penalty,
        "best_of": args.best_of,
        "stop": args.stop
    }
    return payload

def get_response(payload):
    # define your own chatgpt and call it
    response = requests.post(url, json=payload, headers=headers)
    return response.text


def read_prompt_from_json():
    with open("tool_prompt.json", "r", encoding="utf-8") as f:
        prompt = json.load(f)
    return prompt

def read_description_from_json():
    with open("tool_description.json", "r", encoding="utf-8") as f:
        description = json.load(f)
    return description

def read_seed_from_json():
    with open("tool_seeds.json", "r", encoding="utf-8") as f:
        seed = json.load(f)
    return seed



if __name__ == "__main__":
    description, seed = read_description_from_json(), read_seed_from_json()
    description = description[args.tool_name]
    prompt = 'Generate one query about using a tool given the description of the tool' + description +  '\nPlease generate one query for using this tool accroding to the above description:\n'
    queries = []
    tot_num = args.total_num
    fail_num = 0
    while len(queries) < tot_num:
        if fail_num > 100:
            print("fail to get response")
            break
        # get payload
        payload = get_payload(prompt)
        # get response
        try:
            response = get_response(payload)
        except:
            print("error")
            continue
        # save response
        queries.append(response)

    with open("{}_queries.json".format(args.total_num), "w", encoding="utf-8") as f:
        json.dump(queries, f, ensure_ascii=False, indent=4)

