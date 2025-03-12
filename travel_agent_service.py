"""
路由计划指定智能体服务
"""
import os

from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools.file_tools import create_folder, generate_file, exists_folder
from tools.weather_tools import get_weather

# 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
llm = init_chat_model(model="qwen-plus",
                      model_provider="openai",
                      api_key=os.getenv("DASHSCOPE_API_KEY"),
                      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

#如果要指定文件夹名称可以加上:把用户输入的城市名称，作为文件夹名称;
system_prompt = """
用户的输入是一个城市的名称，你是一个旅游博主，需要按照以下步骤进行：
1.需要结合该城市的天气情况，生成一份1天的关于该城市的旅游计划（200字以内）,不要返回Unicode编码格式的字符
2.给该计划起一个标题，该计划文件内容是markdown格式，内存保存在本地文件夹中，文件标题是计划标题，文件后缀是md格式的。

"""

prompt = ChatPromptTemplate.from_messages([
    #SystemMessage(system_prompt),
    ("system", system_prompt),
    ("human", "{location}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# 工具集
tools = [create_folder, exists_folder, generate_file, get_weather]

# 创建agent
agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def invoke_agent(city_name:str):
    # 运行agent
    return agent_executor.invoke({"location": city_name})
