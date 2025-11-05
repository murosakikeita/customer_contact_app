import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from utils import (
    search_company_info_tool,
    search_service_info_tool,
    search_customer_communication_tool,
    search_web_tool,
    search_internal_policy_tool  # ← 新規追加
)

def initialize_environment():
    """環境変数のロード"""
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def initialize_agent_with_tools(agent_enabled: bool):
    """AIエージェントの初期化"""
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    # エージェントを利用する場合のみToolを設定
    if agent_enabled:
        tools = [
            search_company_info_tool,
            search_service_info_tool,
            search_customer_communication_tool,
            search_web_tool,
            search_internal_policy_tool  # ← 追加済
        ]
        agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)
    else:
        agent = None
    return agent
