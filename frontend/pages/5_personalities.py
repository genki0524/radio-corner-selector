import streamlit as st
import traceback
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import api_client
from utils.styles import get_custom_css

st.set_page_config(
    page_title="パーソナリティ管理",
    layout="centered",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("パーソナリティ管理")

# 新規パーソナリティ登録
with st.expander("新規パーソナリティを登録", expanded=False):
    new_name = st.text_input("名前", placeholder="例: 山田太郎", key="new_personality_name")
    new_nickname = st.text_input("ニックネーム（任意）", placeholder="例: たろちゃん", key="new_personality_nickname")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("登録", type="primary", use_container_width=True, key="create_personality_btn"):
            if new_name:
                try:
                    api_client.create_personality(
                        name=new_name,
                        nickname=new_nickname if new_nickname else None
                    )
                    st.success(f"パーソナリティ「{new_name}」を登録しました！")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"登録エラー: {e}")
            else:
                st.warning("名前は必須です")

st.divider()

# パーソナリティ一覧
try:
    personalities = api_client.get_personalities()
    
    st.markdown(f"### 登録済みパーソナリティ ({len(personalities)}名)")
    
    if not personalities:
        st.info("パーソナリティが登録されていません。新しいパーソナリティを登録してください。")
    else:
        # 検索フィルター
        search_query = st.text_input("🔍 検索", placeholder="名前またはニックネームで検索...", key="search_personalities")
        
        # フィルタリング
        filtered_personalities = personalities
        if search_query:
            filtered_personalities = [
                p for p in personalities
                if search_query.lower() in p['name'].lower() or 
                   (p.get('nickname') and search_query.lower() in p['nickname'].lower())
            ]
        
        st.markdown(f"#### 表示中: {len(filtered_personalities)}名")
        
        for personality in filtered_personalities:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    display_name = f"**{personality['name']}**"
                    if personality.get('nickname'):
                        display_name += f" ({personality['nickname']})"
                    st.markdown(display_name)
                
                with col2:
                    col_edit, col_delete = st.columns(2)
                    
                    with col_edit:
                        if st.button("✏️", key=f"edit_btn_{personality['id']}", use_container_width=True, help="編集"):
                            st.session_state[f"editing_{personality['id']}"] = True
                            st.rerun()
                    
                    with col_delete:
                        if st.button("🗑️", key=f"delete_btn_{personality['id']}", use_container_width=True, help="削除"):
                            st.session_state[f"confirm_delete_{personality['id']}"] = True
                            st.rerun()
                
                # 編集フォーム
                if st.session_state.get(f"editing_{personality['id']}", False):
                    with st.container():
                        st.markdown("---")
                        edit_name = st.text_input(
                            "名前",
                            value=personality['name'],
                            key=f"edit_name_{personality['id']}"
                        )
                        edit_nickname = st.text_input(
                            "ニックネーム（任意）",
                            value=personality.get('nickname', ''),
                            key=f"edit_nickname_{personality['id']}"
                        )
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.button("保存", type="primary", key=f"save_{personality['id']}", use_container_width=True):
                                try:
                                    api_client.update_personality(
                                        personality['id'],
                                        {
                                            "name": edit_name,
                                            "nickname": edit_nickname if edit_nickname else None
                                        }
                                    )
                                    st.success("更新しました！")
                                    del st.session_state[f"editing_{personality['id']}"]
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"更新エラー: {e}")
                        
                        with col_cancel:
                            if st.button("キャンセル", key=f"cancel_{personality['id']}", use_container_width=True):
                                del st.session_state[f"editing_{personality['id']}"]
                                st.rerun()
                
                # 削除確認
                if st.session_state.get(f"confirm_delete_{personality['id']}", False):
                    with st.container():
                        st.markdown("---")
                        st.warning(f"⚠️ 本当に「{personality['name']}」を削除しますか？")
                        
                        col_yes, col_no = st.columns(2)
                        with col_yes:
                            if st.button("削除する", key=f"confirm_yes_{personality['id']}", type="primary", use_container_width=True):
                                try:
                                    api_client.delete_personality(personality['id'])
                                    st.success("削除しました")
                                    del st.session_state[f"confirm_delete_{personality['id']}"]
                                    st.rerun()
                                except Exception as e:
                                    traceback.print_exc()
                                    st.error(f"削除エラー: {e}")
                        
                        with col_no:
                            if st.button("キャンセル", key=f"confirm_no_{personality['id']}", use_container_width=True):
                                del st.session_state[f"confirm_delete_{personality['id']}"]
                                st.rerun()
                
                st.markdown("---")

except Exception as e:
    st.error(f"パーソナリティの取得に失敗: {e}")
