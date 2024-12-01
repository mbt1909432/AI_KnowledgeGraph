from pathlib import Path
import sys
from enum import Enum


#project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Directory for data
DATA_DIR = BASE_DIR / 'data'
PROMPTS_DIR = DATA_DIR / 'prompts'
LOG_DIR= DATA_DIR / 'logs'
Raw_Data_DIR = DATA_DIR/"raw_data"

WORKING_DIR = DATA_DIR/"grag_result"#里面存放所有gragrag结果

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)
PROMPTS_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
Raw_Data_DIR.mkdir(exist_ok=True)
WORKING_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / 'graphrag.log'

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = 'INFO'


#YOUR ENDPOINT
END_POINT="YOUR ENDPOINT"

#YOUR API KEY
API_KEY='your_api_key_here'


DEEPSEEK_API_KEY ='your_api_key_here'

MODEL = "deepseek-chat"

#枚举类型
class QueryType(Enum):
    """query type"""
    GLOBAL = "global"#找社区->再找小节点
    LOCAL = "local"#节点描述做召回 找小节点->小节点边->再找社区
    NAIVE = "naive"#传统向量库召回


if __name__=="__main__":
    print(BASE_DIR)
    print(sys.path)

