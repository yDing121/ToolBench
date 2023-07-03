## 使用指导

须填写相关管工具的的description和query示例到tool_descriptions.json和seed_data/**.txt

tool_descriptions里推荐包含的内容：这个tool整体的目的/需求，支持的函数以及每个函数的对应功能（可以直接从对应的api.py里复制），核心函数的返回结果示例（方便chatgpt反向构造）

seed_data/tool_name.txt, 一行一个人工写的query，让chatgpt通过in-context learning构造数据，原则上用户自己写的真实数据，需要提供足够多样的数据，数据量最好>100条。

然后可以运行generate_queries.sh脚本获取数据

数据将保存在output文件夹对应的tool_name文件夹下，可以通过'python deduplication.py --file_path 'your_file_path' '来去重该文件(默认bash脚本中自动运行)

# Data generation via openbmb's code [Windows 10]

## Setup
1. Clone my repo for BMTools and Toolbench
2. Remake all paths so they point in the right place
3. You need API keys
4. Make sure that for both the query and answer directories, there exists a subdirectory for your tool i.e. ToolBench/data-generation/queries/output/<tool name> and ToolBench/data-generation/answer/output/<tool name> exist
5. Create the tool you want to use. Reference any of the tools that have already been made
6. Go to BMTools/bmtools/tools/__init__.py and initialize the new tool: from . import <new tool name>
7. Go to BMTools/host_local_tools.py. Define a loading function (please title it load_<tool name>_tool). Near the end of the file is where all tools are loaded - go there and load the tool by calling the loading function.
8. Go to ToolBench/data-generation/queries/seed_data and enter seeds
9. Go to ToolBench/data-generation/queries/tool_description.json and add the tool description
10. Go to ToolBench/data-generation/queries/incontext.py and either change the default --tool_name option for the parser or edit the run configuration and add --tool_name <tool name> as a launch argument.
11. Specify the total_num of generations to limit API usage
12. Go to ToolBench/data-generation/answer/main_react.py and change the run configuration to include the tool name as well as I/O directories


## Query generation
1. Run ToolBench/data-generation/queries/incontext.py
2. Currently the file is configured to stop every generation cycle and will need an enter. There will be a text prompt indicating an input checkpoint


## Answer generation
1. Run BMTools/host_local_tools.py with no launch arguments in a separate terminal - this is a server
2. Run ToolBench/data-generation/answer/main_react.py
3. Currently the file is configured to stop every generation cycle and will need an enter. There will be a text prompt indicating an input checkpoint


P.S. new generations are appended to the old generation file