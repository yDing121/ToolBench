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
import multiprocessing as mp
import requests
import os
import argparse
import json
import random
import re


parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default="gpt-3.5-turbo", required=False, help='model name')
parser.add_argument('--max_tokens', type=int, default=3072, required=False, help='max tokens')
parser.add_argument('--frequency_penalty', type=float,  default=0, required=False, help='frequency_penalty')
parser.add_argument('--presence_penalty', type=float, required=False, default=0, help='presence_penalty')
parser.add_argument('--best_of', type=int, default=3, required=False, help='best_of')
parser.add_argument('--stop', type=str, default=None, required=False, help='stop')
parser.add_argument('--parallel', type=int, default=1, required=False, help='parallel')
parser.add_argument('--total_num', type=int, default=100, required=False, help='total number of queries')
parser.add_argument('--tool_name', type=str, default="stock", required=False, help='tool name')
parser.add_argument('--language', type=str, default="en", required=True, help="language specified for data creation")
# parser.add_argument('--seed_data_path', type=str, required=False, help="path to seed data, the in-context source data")
parser.add_argument('--cold_start', default=False, action='store_true', help="if cold start, there will be no seed data")
args = parser.parse_args()

def call_chatgpt(prompt):
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

    try_times = 5
    while(try_times > 0):
        try:
            # here, please add your own code for calling LLM (OpenAI) service to get a repsponse
            response = None #  
            break
        except:
            try_times -= 1
            continue
    if try_times == 0:
        raise RuntimeError("Your LLM service is not available.")

    return response.text

def read_description_from_json(tool_name):
    with open("tool_description.json", "r", encoding="utf-8") as f:
        description = json.load(f)[tool_name]
    return description

def read_seed_data(seed_data_path):
    with open(os.path.join("seed_data", seed_data_path), "r", encoding="utf-8") as f:
        seed = [line for line in f.readlines()]
    return seed

if __name__ == "__main__":
    description = read_description_from_json(args.tool_name)
    if not args.cold_start:
        seed_data = read_seed_data(args.tool_name + ".txt")
    saved_queries = []
    tot_num = args.total_num
    fail_num = 0

    dir_path = "output/{}".format(args.tool_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    fout = open(os.path.join(dir_path, "{}_queries.json".format(args.total_num)), "a+", encoding="utf-8")
    
    while len(saved_queries) < tot_num:
        if len(saved_queries) % 500 == 0:
            print("now {} queries".format(len(saved_queries)))
        if args.language == "en":
            prompt = 'Generate 10 queries / instructions about using a tool given the description of the tool and the following examples.\n Description: \n' + description
            if not args.cold_start:
                seed_prompt = random.sample(seed_data, 6)
                seed = "\n".join(seed_prompt)
                prompt += '\nExamples of the queries:\n' + seed
            prompt += '\nOther requirements: (1) Make the generated queries / instructions solvable by the provided tool. (2) You do not need to exactly copy the template or the format of the recommended examples, but must ensure the generated queries / instructions are diverse enough. Please brainstorm and generate novel queries / instructions. (3) The generated queries should simulate the real situation that humans may ask. They can be concise or complex, imperative, rude or polite. Now return the result as a numbered list, e.g., 1. ***\n, 2. ***\n, 3. ***\n, etc. Generate 10 queries or instructions given the above instructions:\n'
        else:
            raise NotImplementedError("language {} not implemented".format(args.language))

        if fail_num > 100:
            print("fail to get response")
            break

        try:
            response = call_chatgpt(prompt)
            response = json.loads(response)["choices"][0]["message"]["content"]
        except:
            print("error")
            fail_num += 1
            continue

        print(prompt)
        print(response)
        response_pattern = re.compile(r'\d+\. (.+?)\n')
        splitted_response = response_pattern.findall(response)
        print(splitted_response)
        for r in splitted_response:
            if r not in saved_queries:
                saved_queries.append(r)
                fout.write(r + "\n")
                fout.flush()
        input()