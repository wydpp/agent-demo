"""
文件和目录操作工具
"""
import json
import os

from langchain_core.tools import tool
from loguru import logger


@tool
def create_folder(folder_name) -> str:
    """
    根据给定的文件夹名称创建文件夹
    :param folder_name: 要创建的文件夹名称
    :return: 创建的文件夹路径
    """
    logger.info(f"调用文件夹创建接口,folder_name={folder_name}")
    try:
        os.mkdir(folder_name)
        return os.path.abspath(folder_name)
    except OSError as e:
        logger.info(f"创建文件夹失败:{e}")
        return ""

@tool
def exists_folder(folder_name) -> bool:
    """
    根据给定的文件夹名称检测文件夹是否存在
    :param folder_name: 要创建的文件夹名称
    :return:
    True表示存在，
    False表示不存在
    """
    logger.info(f"调用文件夹检测接口,folder_name={folder_name}")
    return os.path.exists(folder_name)

@tool
def generate_file(arguments) -> str:
    """
    根据提供的参数生成文件。输入应为 JSON 格式，包含 folder_name、file_name 和 file_content 字段。
    :param arguments: 输入应为 JSON 格式，包含 folder_name、file_name 和 file_content 字段
    :return:
    """
    logger.info(f"创建文件入参：{arguments}")
    if isinstance(arguments, str):
        arguments = json.loads(arguments)
    # 提取参数
    folder_name = arguments.get("folder_name")
    file_name = arguments.get("file_name")
    file_content = arguments.get("file_content")
    if not os.path.exists(folder_name):
        return "文件夹不存在，无法生成文件"

    file_path = os.path.join(folder_name, file_name)
    try:
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(file_content)
        return f"已生成文件:{file_path}"
    except Exception as e:
        return f"生成出错:{str(e)}"