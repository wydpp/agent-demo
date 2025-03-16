import os
from datetime import datetime
from typing import List

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool


@tool
def get_time() -> str:
    """
    返回当前时间，精确到秒
    :return: 当前时间字符串，示例：2024-10-12 14:30:45
    """
    now = datetime.now()
    print("返回当前日期")
    return now.strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_doctor(date: str) -> List[str]:
    """
    返回指定日期，坐诊的医生名称
    :param date: 日期，示例：2023-01-02
    :return: 医生名称列表
    """
    print(f"返回{date}坐诊的医生列表")
    return ["张三", "李四"]


@tool
def hospital_appointment(date: str, doctor_name: str) -> bool:
    """
    医院预约挂号接口
    :param date: 预约日期 ,示例：2023-01-02
    :param doctor_name: 医生名名称
    :return: 预约结果,true:成功，false：失败
    """
    if doctor_name == "张三":
        print("张三医生没号了")
        return False
    return True


tools = [get_time, get_doctor, hospital_appointment]

# 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
llm = init_chat_model(model="qwen-max",
                      model_provider="openai",
                      api_key=os.getenv("DASHSCOPE_API_KEY"),
                      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

system_prompt = """
你是一个人工智能体，请自主处理用户的信息
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({"input": "生病了，我要预约一个明天的号?"})
print(result)
