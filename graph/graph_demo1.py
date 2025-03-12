import os
from typing import Annotated, Literal

from langchain.chat_models import init_chat_model
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

from tools.weather_tools import get_weather


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph = StateGraph(State)

tools = [get_weather]

llm = init_chat_model(model="qwen-plus",
                      model_provider="openai",
                      api_key=os.getenv("DASHSCOPE_API_KEY"),
                      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

llm_with_tools = llm.bind_tools(tools)

# 工具node
tool_node = ToolNode(tools)
graph.add_node("tool_node", tool_node)


def prompt_node(state: State) -> State:
    new_messages = llm_with_tools.invoke(state["messages"])
    return State(messages=[new_messages])
graph.add_node("prompt_node",prompt_node)

def conditional_node(state:State) -> Literal["tool_node","__end__"]:
    last_message  = state["messages"][-1]
    print(f"last_message: {last_message}")
    if last_message.tool_calls:
        return "tool_node"
    else:
        return "__end__"
graph.add_conditional_edges("prompt_node",conditional_node)
graph.add_edge("tool_node","prompt_node")
graph.set_entry_point("prompt_node")


APP = graph.compile()

new_state = APP.invoke(State(messages=["合肥的天气怎么样?"]))

print(new_state["messages"][-1].content)

