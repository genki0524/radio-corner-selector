"""
ラジオ投稿管理アプリ - ダッシュボード
"""
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

st.title("ラジオ投稿ダッシュボード")
st.markdown("日々のメモを記録し、最適なコーナーへ投稿しましょう")

st.divider()

# クイックメモ入力
st.subheader("クイックメモ")
col1, col2 = st.columns([4, 1])
with col1:
    memo_content = st.text_area(
        "次のコーナーのネタを書き留める...",
        height=120,
        label_visibility="collapsed",
        placeholder="例: 駅前の新しいカフェでおいしいコーヒーを飲んだ...",
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

# 統計カード
st.subheader("投稿統計")
try:
    stats = api_client.get_mail_stats()
    draft_count = stats.get("draft", 0)
    sent_count = stats.get("sent", 0)
    accepted_count = stats.get("accepted", 0)
    rejected_count = stats.get("rejected", 0)
except Exception as e:
    st.error(f"統計データの取得に失敗: {e}")
    draft_count = sent_count = accepted_count = rejected_count = 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="card" style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <h3 style="font-size: 0.875rem; margin-bottom: 0.5rem; opacity: 0.9;">下書き</h3>
            <p style="font-size: 2.5rem; font-weight: 700; margin: 0;">{draft_count}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="card" style="text-align: center; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white;">
            <h3 style="font-size: 0.875rem; margin-bottom: 0.5rem; opacity: 0.9;">送信済み</h3>
            <p style="font-size: 2.5rem; font-weight: 700; margin: 0;">{sent_count}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="card" style="text-align: center; background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white;">
            <h3 style="font-size: 0.875rem; margin-bottom: 0.5rem; opacity: 0.9;">採用</h3>
            <p style="font-size: 2.5rem; font-weight: 700; margin: 0;">{accepted_count}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
        <div class="card" style="text-align: center; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white;">
            <h3 style="font-size: 0.875rem; margin-bottom: 0.5rem; opacity: 0.9;">不採用</h3>
            <p style="font-size: 2.5rem; font-weight: 700; margin: 0;">{rejected_count}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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

# サイドバー
with st.sidebar:
    st.header("クイックアクション")
    if st.button("新規メモ作成", use_container_width=True, type="primary"):
        st.switch_page("pages/1_memos.py")
    if st.button("メール作成", use_container_width=True):
        st.switch_page("pages/3_mail.py")
    if st.button("番組を追加", use_container_width=True):
        st.switch_page("pages/2_programs.py")
    
    st.divider()
    
    st.header("ヘルプ")
    st.markdown("""
    **使い方:**
    1. メモを記録する
    2. AIが最適なコーナーを提案
    3. メールを作成して送信
    4. 採用/不採用を記録
    """)