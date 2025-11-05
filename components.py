import streamlit as st

def render_sidebar():
    """サイドバー設定を描画"""
    st.sidebar.header("設定")

    agent_enabled = st.sidebar.radio(
        "AIエージェント機能の利用",
        ["利用する", "利用しない"],
        index=0
    ) == "利用する"

    inquiry_mode = st.sidebar.toggle("問い合わせモード", value=False)

    st.sidebar.markdown("---")
    st.sidebar.info("※ 問い合わせモードをONにするとSlackに通知されます。")

    return agent_enabled, inquiry_mode


def render_chat_ui():
    """チャット欄を描画"""
    st.write("### 💬 チャット")
    user_input = st.text_area("質問を入力してください：", placeholder="例：システムにログインできません。対応方法を教えてください。")
    if st.button("送信"):
        return user_input.strip()
    return None
