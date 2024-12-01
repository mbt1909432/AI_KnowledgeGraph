import logging
import os
import sys
from pathlib import Path
from time import time
from openai import AsyncOpenAI

path=str(Path(__file__).resolve().parent.parent.parent)
sys.path.append(path)
print(path)

from config.settings import PROMPTS_DIR,END_POINT,API_KEY

STORY_PROMPT=PROMPTS_DIR/"story_ai.txt"

from openai import AsyncOpenAI
import asyncio


def read_prompt()->str:
    with STORY_PROMPT.open("r", encoding='utf-8') as file:
        return file.read()





async def call_agent(query:str):
    client = AsyncOpenAI(api_key=API_KEY, base_url=END_POINT,default_headers={"x-foo": "true"})
    print("-----当前prompt为-----------")
    print(read_prompt())
    print("-----当前query为-----------")
    print(query)

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": read_prompt()},
            {"role": "user", "content": query},#请用make sure造句，还有你造句的索引
        ],
        stream=False,

    )
    result = response.choices[0].message.content
    return result


if __name__=="__main__":
    data= {'result': '中飢渴苦常逼登上大火山長受無量苦或有七寶剎平正住莊嚴清淨業力起微妙善安隱彼佛剎土中唯見人天趣功德果成就常受諸快樂一'}
    asyncio.run(call_agent(data['result']))


