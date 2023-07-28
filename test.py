from langchain.agents import AgentType, initialize_agent
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.llms import OpenAI
from my_utils.load_keys import load_key




@tool("weather", return_direct=False)
def weather(location: str) -> str:
    """
    Return today's weather at the requested location

    :param location: location to get weather for
    :return: today's weather for the inputted location
    """
    return "TOOL CALLED! Sunny, 45 C, mild winds"



zero_shot_extracted_prompt = """
Answer the following questions as best you can. You have access to the following tools:

weather: weather(location: str) -> str - Return today's weather at the requested location

    :param location: location to get weather for
    :return: today's weather for the inputted location

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [weather]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
ch_zero_shot_extracted_prompt = """
开始回答以下问题。您可以使用以下工具：

Weather: weather(location: str) -> str - 返回所请求位置今天的天气情况

    :param location: 要获取天气的位置
    :return: 输入位置今天的天气

请使用以下格式：

Question: 您必须回答的输入问题
Thought: 您应该始终考虑该做什么
Action: 要执行的动作，应为 [weather] 中的一个
Action Input: Action的输入
Observation: Action的结果
...（这个Thought/Action/Action Input/Observation可以重复 N 次）
Thought: 我现在知道最终答案了
Final Answer: 原始输入问题的最终答案

开始！

问题：{input}
思考：{agent_scratchpad}
"""
chat_zero_shot_extracted_prompt = """
Answer the following questions as best you can. You have access to the following tools:

weather: weather(location: str) -> str - Return today's weather at the requested location

    :param location: location to get weather for
    :return: today's weather for the inputted location

The way you use the tools is by specifying a json blob.
Specifically, this json should have a `action` key (with the name of the tool to use) and a `action_input` key (with the input to the tool going here).

The only values that should be in the "action" field are: weather

The $JSON_BLOB should only contain a SINGLE action, do NOT return a list of multiple actions. Here is an example of a valid $JSON_BLOB:

```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```

ALWAYS use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action:
```
$JSON_BLOB
```
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Reminder to always use the exact characters `Final Answer` when responding.
"""
ch_chat_zero_shot_extracted_prompt = """
请尽力回答以下问题。您可以使用以下工具：

Weather: weather(location: str) -> str - 返回所请求位置今天的天气情况

    :param location: 要获取天气的位置
    :return: 输入位置今天的天气

您可以通过指定一个 JSON 块来使用这些工具。具体来说，这个JSON块应该有一个 `action` 键（要使用的工具名称）和一个 `action_input` 键（传递给工具的内容）。

"action" 字段中应该只有以下值：[weather]

JSON块中只能包含一个动作，不要返回含有多个动作的列表。以下是一个有效的JSON块示例：

```
{{
  "action": $工具名称,
  "action_input": $输入
}}
```

请始终使用以下格式：

Question: 您必须回答的输入问题
Thought: 您应该始终考虑该做什么
Action: 
```
JSON块
```
Observation: Action的结果
...（这个Question/Thought/Observation可以重复 N 次）
Thought：我现在知道最终答案了
Final Answer：原始输入问题的最终答案

开始！请在做最终回答时使用 `最终答案`字段。
"""

if __name__ == "__main__":
    load_key("openai")
    tools = [
        weather
    ]
    llm = OpenAI(temperature=0)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    agent.run("How's the weather in shenzhen today?")
