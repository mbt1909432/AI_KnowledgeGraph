
from fastapi import FastAPI,Query, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import nest_asyncio



nest_asyncio.apply()

#component
from ai.Gen_KG import graph_rag
from  config import settings
from ai.Gen_KG import story_agent

#uvicorn app:app --reload --host 0.0.0.0
app = FastAPI()

result_cache=None#故事机器人用

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头部
)




class KGQueryRequest(BaseModel):
    query: str
    type:str

class KGGenerationRequest(BaseModel):
    src_path: str  # 原文本的位置位于？
    dest_path: str  # 最终生成的目录位于？
    text: str

#目前demo用不上
@app.post("/KG_Generation")
async def KG_Generation():
    print("A")
    return {"message": "POST 请求成功"}


@app.post("/KG_Talk")
async def KG_Talk(query:KGQueryRequest):
    global result_cache
    if query.type==settings.QueryType.LOCAL.value:
        result = graph_rag.query(query.query+"(请用中文回答)", settings.QueryType.LOCAL)
        result_cache=result
    elif query.type==settings.QueryType.GLOBAL.value:
        result = graph_rag.query(query.query+"(请用中文回答)", settings.QueryType.GLOBAL)
        result_cache = result
    else:
        return  {"result":"你的请求无效"}
    print("---------------")
    print(result_cache)
    print("---------------")
    return result



@app.get("/KG_Story")
async def KG_Story():
    print("---------------")
    print(result_cache)
    print("---------------")
    if result_cache:
        response=await story_agent.call_agent(result_cache['result'])
        return {"result": response}
    else:
        return {"result": "你还没有提问！无法生成故事"}


class modifier(BaseModel):
    query: str

@app.post("/modify_text")
async def modify_text(query:modifier):
    with open(rf"E:\pycharm_project\AI_KnowledgeGraph\FrontendCode\final1\data.txt",'w',encoding='utf-8') as f:
        f.write(query.query)
        print(f"修改结果为{query.query}")

@app.get("/read_text")
async def read_text():
    with open(rf"E:\pycharm_project\AI_KnowledgeGraph\FrontendCode\final1\data.txt",'r',encoding='utf-8') as f:
        result=f.read()
        print(f"读取结果为{result}")
        return {"content": result}  # 返回文件内容作为 JSON 响应





if __name__=="__main__":
    pass


