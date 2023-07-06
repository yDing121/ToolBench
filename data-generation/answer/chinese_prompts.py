# flake8: noqa
CPREFIX = """尽你所能回答以下的问题。你可以使用以下的API接口："""
CFORMAT_INSTRUCTIONS = """请使用以下的格式:

Question: 你需要回答的问题
Thought: 做任何操作之前你都需要进行思考
Action: 你可以进行的操作，必须从以下的集合中选择 [{tool_names}]
Action Input: 操作的相关输入
Observation: 进行操作之后的观察
... (这个 Thought/Action/Action Input/Observation 循环可以执行 N 次)

尽你所能在最终答案中提供有用的信息。在任何情况下都不能编造答案。如果你的观察没有源链接，不要伪造一个链接。
如果你觉得你收集的信息足以回答问题了，请使用：
Thought: 我有足够的信息了
Final Answer: 你对一开始的问题的最终答案"""
CSUFFIX = """开始吧！记得你能使用的工具都在以上的集合内，请不要使用其他的工具。

Question: {input}
Thought:{agent_scratchpad}"""
