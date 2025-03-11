"""
LangChain 一些接口使用示例
https://python.langchain.com/docs/how_to/
"""
import os

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from tools.weather_tools import get_weather

# Create the agent
# 记忆功能
memory = MemorySaver()
# 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
llm = init_chat_model(model="qwen-plus",
                      model_provider="openai",
                      api_key=os.getenv("DASHSCOPE_API_KEY"),
                      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
# 可使用的工具列表
tools = [get_weather]
# 创建了一个agent
agent_executor = create_react_agent(llm, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}
# 普通输出
# response = agent_executor.invoke({"messages": [HumanMessage(content="北京天气怎么样")]}, config)
# print(response)
# 流式输出
for step in agent_executor.stream(
        {"messages": [HumanMessage(content="北京天气怎么样")]},
        config=config,
        stream_mode="values",
):
    step["messages"][-1].pretty_print()
    print(step)
