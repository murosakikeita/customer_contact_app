import json
import datetime
import os
import openai
from langchain.tools import Tool
from langchain.utilities import SerpAPIWrapper
from slack_sdk import WebClient

# =====================================================
# 🔍 RAGデータ検索関数（ダミー）
# =====================================================
def search_rag_data(folder_path: str, query: str):
    """RAGデータフォルダから検索するダミー関数"""
    return f"[{folder_path}] に関する検索結果: {query}"

# =====================================================
# 🧰 各Tool定義
# =====================================================

search_company_info_tool = Tool(
    name="search_company_info_tool",
    description="株式会社EcoTeeに関する情報を参照するためのツール",
    func=lambda q: search_rag_data("data/rag/company", q)
)

search_service_info_tool = Tool(
    name="search_service_info_tool",
    description="自社サービスEcoTeeに関する情報を参照するためのツール",
    func=lambda q: search_rag_data("data/rag/service", q)
)

search_customer_communication_tool = Tool(
    name="search_customer_communication_tool",
    description="顧客とのやり取りに関する情報を参照するためのツール",
    func=lambda q: search_rag_data("data/rag/customer", q)
)

search_web_tool = Tool(
    name="search_web_tool",
    description="Web検索を行うためのツール",
    func=lambda q: SerpAPIWrapper().run(q)
)

# 新しく追加したTool（課題①対応）
search_internal_policy_tool = Tool(
    name="search_internal_policy_tool",
    description="社内規定やポリシーに関する情報を参照するためのツール",
    func=lambda q: search_rag_data("data/rag/policy", q)
)

# =====================================================
# 💬 ユーザー入力処理
# =====================================================
def handle_user_message(user_input, agent, agent_enabled):
    """ユーザーの質問に対して回答を生成"""
    if agent_enabled and agent is not None:
        return agent.run(user_input)
    else:
        return f"（AIエージェントOFF）検索結果: {search_rag_data('data/rag', user_input)}"

# =====================================================
# 🔔 Slack通知機能（課題②対応済み）
# =====================================================
def notice_slack(inquiry_content, ai_response):
    """Slackに問い合わせ内容を通知"""
    slack_token = os.getenv("SLACK_USER_TOKEN")
    if not slack_token:
        print("⚠️ Slackトークンが設定されていません (.env を確認してください)")
        return

    client = WebClient(token=slack_token)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    prompt = f"""
    以下の問い合わせ内容に対して、適切な担当者を選定した理由を説明してください。
    問い合わせ内容: {inquiry_content}
    """

    # OpenAI API呼び出し（旧形式：openai==0.27.x）
    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは社内サポート担当AIです。"},
                {"role": "user", "content": prompt}
            ]
        )
        mention_reason = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        mention_reason = f"（メンション理由生成中にエラー: {e}）"

    # Slack送信本文
    message = f"""
こちらは顧客問い合わせに対しての「担当者割り振り」と「回答・対応案の提示」を自動で行うAIアシスタントです。
担当者は問い合わせ内容を確認し、対応してください。

============================
【問い合わせ情報】
・問い合わせ内容: {inquiry_content}
・日時: {timestamp}
----------------------------
【メンション先の選定理由】
{mention_reason}
----------------------------
【回答・対応案】
{ai_response}
----------------------------
【参照資料】
・従業員情報.csv
・問い合わせ履歴.csv
"""

    try:
        client.chat_postMessage(channel="#動作検証用", text=message)
        print("✅ Slack通知を送信しました。")
    except Exception as e:
        print(f"⚠️ Slack通知エラー: {e}")
