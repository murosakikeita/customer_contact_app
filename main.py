import streamlit as st
from initialize import initialize_environment, initialize_agent_with_tools
from components import render_sidebar, render_chat_ui
from utils import handle_user_message, notice_slack
from constants import APP_TITLE

# -------------------------------
# Streamlitアプリ設定
# -------------------------------
st.set_page_config(page_title=APP_TITLE, layout="wide")

# 初期設定の実行
initialize_environment()

# サイドバーの描画（AIエージェント機能の利用有無、問い合わせモード）
agent_enabled, inquiry_mode = render_sidebar()

# チャット画面の描画
st.title(APP_TITLE)
user_input = render_chat_ui()

# エージェントの初期化
agent = initialize_agent_with_tools(agent_enabled)

# -------------------------------
# ユーザー入力の処理
# -------------------------------
if user_input:
    with st.spinner("AIが応答を生成中..."):
        response = handle_user_message(user_input, agent, agent_enabled)

    st.markdown(f"**AIの回答:** {response}")

    # 問い合わせモードがONならSlack通知を実施
    if inquiry_mode:
        notice_slack(user_input, response)
