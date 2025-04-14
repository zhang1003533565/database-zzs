import os
from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(
        temperature=0,
        model="deepseek-chat",  # ✅ DeepSeek 官方模型名称
        openai_api_key=os.getenv("OPENAI_API_KEY", "sk-9dad3f4d97504097a2e24a863814272a"),
        openai_api_base="https://api.deepseek.com"  # ✅ 不加 /v1
    )
