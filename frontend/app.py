import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils.api_client import api_client
from utils.styles import get_custom_css

st.set_page_config(
    page_title="ラジオ投稿ダッシュボード",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

# クイックメモ入力
st.subheader("クイックメモ")
col1, col2 = st.columns([4, 1])
with col1:
    memo_content = st.text_area(
        "次のコーナーのネタを書き留める...",
        height=120,
        label_visibility="collapsed",
        key="quick_memo_input"
    )
with col2:
    st.write("")
    st.write("")
    if st.button("追加", use_container_width=True, type="primary"):
        if memo_content.strip():
            try:
                api_client.create_memo(memo_content)
                st.success("メモを追加しました！")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"エラー: {e}")
        else:
            st.warning("メモの内容を入力してください")

st.divider()

# 最近のメモ
st.subheader("最近のメモ")
try:
    memos = api_client.get_memos(limit=3)
    
    if not memos:
        st.info("メモがありません。新しいメモを作成してください。")
    else:
        for memo in memos:
            from datetime import datetime
            created_at = datetime.fromisoformat(memo['created_at'].replace('Z', '+00:00'))
            st.markdown(
                f"""
                <div class="memo-card">
                    <p style="color: #1f2937; font-weight: 500; margin-bottom: 0.5rem; line-height: 1.6;">
                        {memo['content'][:100]}{'...' if len(memo['content']) > 100 else ''}
                    </p>
                    <p style="color: #9ca3af; font-size: 0.75rem; margin: 0;">
                        作成日時: {created_at.strftime('%Y年%m月%d日 %H:%M')}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
except Exception as e:
    st.error(f"メモの取得に失敗: {e}")

col1, col2 = st.columns(2)
with col1:
    if st.button("すべてのメモを見る", use_container_width=True):
        st.switch_page("pages/1_memos.py")
with col2:
    if st.button("番組管理", use_container_width=True):
        st.switch_page("pages/2_programs.py")