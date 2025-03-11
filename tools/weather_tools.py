"""
获取天气的工具
"""
from langchain_core.tools import tool
from loguru import logger


@tool
def get_weather(city_name: str):
    """
    根据城市名称获取城市天气信息接口
    :param city_name: 城市名称
    :return: 城市天气信息
    """
    logger.info(f"调用天气查询工具,city_name={city_name}")
    if city_name == "合肥" or city_name == "合肥市":
        return {"weather_summary": "天气晴朗，5~22℃，东南风2级，空气质量良"}
    else:
        return {"weather_summary": "中雨，1~10℃，西北风3级，空气质量差"}
