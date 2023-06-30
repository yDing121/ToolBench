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

import json
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--file_path', type=str, default="./output/stock/stock.txt", required=True, help='file path')
args = parser.parse_args()
print(args.file_path)

if __name__ == '__main__':
    #read the file and deduplicate the line and rewrite the file

    with open(args.file_path, 'r') as f:
        lines = f.readlines()
        print(lines)
    lines = list(set(lines))
    print(lines)
    with open(args.file_path, 'w') as f:
        f.writelines(lines)
