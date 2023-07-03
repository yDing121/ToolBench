import langchain
import sys
import jsonlines
from math import floor
import argparse
import multiprocessing as mp

from langchain import LLMChain
from langchain.agents import ZeroShotAgent

sys.path.insert(0, "D:/Coding/BMTools")
from src import load_keys
from bmtools.agent.executor import Executor
from bmtools import get_logger
from utils import prepare_queries, NAME2URL, MyZeroShotAgent, MyAgentExecutor, MyMRKLOutputParser, LogParser
from bmtools.agent.singletool import import_all_apis, load_single_tools

logger = get_logger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--tool_name', type=str, default="", required=False, help='tool name')
parser.add_argument('--input_query_file', type=str, default="", required=False, help='input path')
parser.add_argument('--output_answer_file', type=str, default="", required=False, help='output path')
parser.add_argument('--process_num', type=int, default=1, required=False, help='process number')
parser.add_argument('--debug', type=int, default=0, required=False, help='1 for debugging')
args = parser.parse_args()

# Keys
# # OpenAI
# with open("D:/Coding/key.txt", "r") as fin:
#     os.environ["OPENAI_API_KEY"] = fin.readline()
load_keys.load_key("openai")

# basically copy the codes in singletool.py
class STQuestionAnswerer:
    def __init__(self, stream_output=False, llm_model=None):
        self.llm = llm_model
        self.stream_output = stream_output

    def load_tools(self, name, meta_info, prompt_type="react-with-tool-description", return_intermediate_steps=True):
        self.all_tools_map = {}
        self.all_tools_map[name] = import_all_apis(meta_info)

        logger.info("Tool [{}] has the following apis: {}".format(name, self.all_tools_map[name]))

        tool_str = "; ".join([t.name for t in self.all_tools_map[name]])
        prefix = f"""Answer the following questions as best you can. Specifically, you have access to the following APIs:"""
        suffix = """Begin! Remember: (1) Follow the format, i.e,\nThought:\nAction:\nAction Input:\nObservation:\nFinal Answer:\n (2) Provide as much as useful information in your Final Answer. (3) Do not make up anything, and if your Observation has no link, DO NOT hallucihate one. (4) If you have enough information and want to stop the process, please use \nThought: I have got enough information\nFinal Answer: **your response. \n The Action: MUST be one of the following:""" + tool_str + """\nQuestion: {input}\n Agent scratchpad (history actions):\n {agent_scratchpad}"""

        prompt = ZeroShotAgent.create_prompt(
            self.all_tools_map[name], 
            prefix=prefix, 
            suffix=suffix, 
            input_variables=["input", "agent_scratchpad"]
        )
        llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt
        )
        logger.info("Full prompt template: {}".format(prompt.template))
        tool_names = [tool.name for tool in self.all_tools_map[name] ]
        agent = MyZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
        agent.output_parser = MyMRKLOutputParser()
        if self.stream_output:
            agent_executor = Executor.from_agent_and_tools(agent=agent, tools=self.all_tools_map[name] , verbose=True, return_intermediate_steps=return_intermediate_steps)
        else:
            agent_executor = MyAgentExecutor.from_agent_and_tools(agent=agent, tools=self.all_tools_map[name], verbose=True, return_intermediate_steps=return_intermediate_steps)
        
        agent_executor.early_stopping_method = "generate"
        
        return agent_executor, prompt.template
        

def main(process_id):
    if tool_name not in NAME2URL:
        tool_url = f"http://127.0.0.1:8079/tools/{tool_name}/"
    else:
        tool_url = NAME2URL[tool_name]
    tools_name, tools_config = load_single_tools(tool_name, tool_url)
    print(tools_name, tools_config)

    # # this CustomLLM is basically a ChatGPT, we cannot provide the code here, please use your own ChatGPT for answer generation
    # customllm = CustomLLM()
    customllm = langchain.OpenAI(temperature=0)

    qa = STQuestionAnswerer(llm_model=customllm)
    agent, prompt_template = qa.load_tools(tools_name, tools_config)
    agent.return_intermediate_steps = True

    log_parser = LogParser()
    if process_id + 1 == process_num:
        cur_queries = queries[process_id*split_size:]
    else:
        cur_queries = queries[process_id*split_size: (process_id+1)*split_size]
    for query in cur_queries:
        out_dict = {
            "prompt": prompt_template,
            "query": query,
            "chains": []
        }
        output = agent(inputs=query)
        # 我们提前parse一遍，为了防止后面的parse出错，额外把intermediate_steps也保存了
        intermediate_steps = output["intermediate_steps"]
        for i,step in enumerate(intermediate_steps):
            log = step[0][-1]
            parsed_output = log_parser.parse(log)._asdict()
            thought = parsed_output["thought"][0]
            action = parsed_output["action"][0]
            action_input = parsed_output["action_input"][0]
            if action_input == "":
                action_input = step[0][1]
            observation = step[1]

            chain = {
                "thought": thought,
                "action": action,
                "action_input": action_input,
                "observation": observation,
            }
            out_dict["chains"].append(chain)
        out_dict["answer"] = output["output"]
        out_dict["intermediate_steps"] = output["intermediate_steps"]
        out_dict["log"] = output["log"]
        out_file.write(out_dict)
        input("Input checkpoint: press enter to continue")


process_num = args.process_num
tool_name = args.tool_name
input_query_file = args.input_query_file
output_answer_file = args.output_answer_file
debug = args.debug

# load input queries, and filter already generated queries in ${output_answer_file}
queries = prepare_queries(input_query_file, output_answer_file) 
split_size = int(floor(len(queries) / process_num))
out_file = jsonlines.open(output_answer_file, "a")
out_file._flush = True

if __name__=='__main__':
    if debug == 1:
        main(0)
    else:
        with mp.Pool(processes=process_num) as pool:
            pool.map(main, range(process_num))