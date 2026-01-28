import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import api_client
from utils.styles import get_custom_css

st.set_page_config(
    page_title="メモ一覧",
    layout="centered",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("メモ一覧")

# 検索・フィルター
col1, col2 = st.columns([3, 1])
with col1:
    search_query = st.text_input("メモを検索", placeholder="キーワードを入力...")
with col2:
    filter_option = st.selectbox(
        "フィルター",
        ["すべて", "未処理", "振り分け済み"],
    )

st.divider()

# 新規メモ作成
with st.expander("新しいメモを作成", expanded=False):
    new_memo_content = st.text_area(
        "メモの内容",
        height=150,
        placeholder="ネタや気づきを書き留めてください...",
        key="new_memo_content"
    )
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("保存", type="primary", use_container_width=True):
            if new_memo_content.strip():
                try:
                    api_client.create_memo(new_memo_content)
                    st.success("メモを保存しました！")
                    st.rerun()
                except Exception as e:
                    st.error(f"エラー: {e}")
            else:
                st.warning("メモの内容を入力してください")
    with col2:
        if st.button("キャンセル", use_container_width=True):
            st.rerun()

st.divider()

# メモ一覧
try:
    memos = api_client.get_memos()
    
    # 検索フィルタリング
    if search_query:
        memos = [m for m in memos if search_query.lower() in m["content"].lower()]
    
    st.markdown(f"### メモ ({len(memos)}件)")
    
    if not memos:
        st.info("メモがありません。新しいメモを作成してください。")
    else:
        for memo in memos:
            with st.container():
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    created_at = datetime.fromisoformat(memo['created_at'].replace('Z', '+00:00'))
                    st.markdown(
                        f"""
                        <div class="memo-card">
                            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
                                <span class="badge badge-primary">ID: {memo['id']}</span>
                                <span style="color: #9ca3af; font-size: 0.75rem;">
                                    {created_at.strftime('%Y/%m/%d %H:%M')}
                                </span>
                            </div>
                            <p style="color: #1f2937; font-weight: 500; line-height: 1.6; margin-bottom: 0.5rem;">
                                {memo['content']}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("メール作成", key=f"mail_{memo['id']}", use_container_width=True):
                        st.session_state["selected_memo_id"] = memo["id"]
                        st.switch_page("pages/3_mail.py")
                    
                    if st.button("削除", key=f"delete_{memo['id']}", use_container_width=True):
                        try:
                            api_client.delete_memo(memo['id'])
                            st.success(f"メモ {memo['id']} を削除しました")
                            st.rerun()
                        except Exception as e:
                            st.error(f"削除エラー: {e}")
except Exception as e:
    st.error(f"メモの取得に失敗: {e}")
