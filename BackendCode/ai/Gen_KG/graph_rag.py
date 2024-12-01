import logging
import os
import sys
from pathlib import Path
from time import time

from openai import AsyncOpenAI
from nano_graphrag import GraphRAG, QueryParam
from nano_graphrag.base import BaseKVStorage
from nano_graphrag._utils import compute_args_hash
import nano_graphrag.prompt

path=str(Path(__file__).resolve().parent.parent.parent)
sys.path.append(path)
print(path)

from config.settings import QueryType,Raw_Data_DIR,WORKING_DIR,DEEPSEEK_API_KEY,MODEL
from ai.Gen_KG.prompt_modification import PromptModifier,PromptType


CURRENT_WORKING_DIRECTORY=str(WORKING_DIR/"demo_result")
#当前跑后存放的文件夹

#当前数据的路径
CURRENT_DATA_PATH=str(Raw_Data_DIR/"merged_output.txt")

current_prompt=PromptModifier(PromptType.Entity_Extraction)


nano_graphrag.prompt.PROMPTS["DEFAULT_ENTITY_TYPES"]=["宝石","功效"]
nano_graphrag.prompt.PROMPTS["entity_extraction"]=current_prompt.prompt#modify_prompt(r"prompts/1entity_extraction.txt")


logging.basicConfig(level=logging.WARNING)
logging.getLogger("nano-graphrag").setLevel(logging.INFO)



async def deepseepk_model_if_cache(
    prompt, system_prompt=None, history_messages=[], **kwargs
) -> str:
    openai_async_client = AsyncOpenAI(
        api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"
    )
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # Get the cached response if having-------------------
    hashing_kv: BaseKVStorage = kwargs.pop("hashing_kv", None)
    messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})
    if hashing_kv is not None:
        args_hash = compute_args_hash(MODEL, messages)
        if_cache_return = await hashing_kv.get_by_id(args_hash)
        if if_cache_return is not None:
            return if_cache_return["return"]
    # -----------------------------------------------------

    response = await openai_async_client.chat.completions.create(
        model=MODEL, messages=messages, **kwargs
    )

    # Cache the response if having-------------------
    if hashing_kv is not None:
        await hashing_kv.upsert(
            {args_hash: {"return": response.choices[0].message.content, "model": MODEL}}
        )
    # -----------------------------------------------------
    return response.choices[0].message.content


def remove_if_exist(file):
    if os.path.exists(file):
        os.remove(file)


def query(query:str,query_type:QueryType):

    start = time()
    rag = GraphRAG(
        working_dir=CURRENT_WORKING_DIRECTORY,
        best_model_func=deepseepk_model_if_cache,
        cheap_model_func=deepseepk_model_if_cache,
        #embedding_func=local_embedding
    )
    query_result=rag.query(query, param=QueryParam(mode=query_type.value) )

    print(fr"当前query类型:{query_type.value},query time:", time() - start)
    return {"result":query_result}


def insert(path:str):

    with open(path, encoding="utf-8-sig") as f:
        FAKE_TEXT = f.read()

    remove_if_exist(f"{CURRENT_WORKING_DIRECTORY}/vdb_entities.json")
    remove_if_exist(f"{CURRENT_WORKING_DIRECTORY}/kv_store_full_docs.json")
    remove_if_exist(f"{CURRENT_WORKING_DIRECTORY}/kv_store_text_chunks.json")
    remove_if_exist(f"{CURRENT_WORKING_DIRECTORY}/kv_store_community_reports.json")
    remove_if_exist(f"{CURRENT_WORKING_DIRECTORY}/graph_chunk_entity_relation.graphml")

    rag = GraphRAG(
        working_dir=CURRENT_WORKING_DIRECTORY,
        enable_llm_cache=True,
        best_model_func=deepseepk_model_if_cache,
        cheap_model_func=deepseepk_model_if_cache,
        #embedding_func=local_embedding
    )
    start = time()
    rag.insert(FAKE_TEXT)
    print("indexing time:", time() - start)
    # rag = GraphRAG(working_dir=WORKING_DIR, enable_llm_cache=True)
    # rag.insert(FAKE_TEXT[half_len:])


if __name__ == "__main__":
    #print(nano_graphrag.prompt.PROMPTS["DEFAULT_ENTITY_TYPES"])
    #insert(CURRENT_DATA_PATH)
    #print("A")
    print(query("这关于什么的，用中文回答",QueryType.GLOBAL))



