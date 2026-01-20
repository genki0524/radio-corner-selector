"""
番組管理ページ
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import api_client
from utils.styles import get_custom_css

st.set_page_config(
    page_title="番組管理",
    page_icon="📺",
    layout="centered",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("番組・コーナー管理")

# 番組検索・フィルター
st.subheader("番組を絞り込む")
col1, col2 = st.columns(2)

with col1:
    try:
        personalities = api_client.get_personalities()
        personality_options = ["全てのパーソナリティ"] + [
            f"{p['name']}" + (f" ({p['nickname']})" if p.get('nickname') else "")
            for p in personalities
        ]
        selected_personality = st.selectbox("パーソナリティ", personality_options)
    except Exception as e:
        st.error(f"パーソナリティの取得に失敗: {e}")
        personalities = []
        selected_personality = "全てのパーソナリティ"

with col2:
    program_search = st.text_input("番組名 (部分一致)", placeholder="番組名を入力...")

st.divider()

# 新規番組登録
with st.expander("新規番組を登録", expanded=False):
    st.markdown("#### 基本情報")
    
    new_program_title = st.text_input("番組名", placeholder="例: オールナイトニッポン", key="new_program_title")
    
    col1, col2 = st.columns(2)
    with col1:
        new_program_email = st.text_input("投稿用メールアドレス", placeholder="example@radio.com", key="new_program_email")
    with col2:
        new_program_schedule = st.text_input("放送スケジュール", placeholder="例: 月〜金 6:00-10:00", key="new_program_schedule")
    
    # パーソナリティ選択
    personality_names = [p['name'] for p in personalities]
    selected_personalities = st.multiselect("パーソナリティ", personality_names, key="selected_personalities")
    
    st.markdown("#### コーナー設定")
    num_corners = st.number_input("コーナー数", min_value=0, max_value=10, value=1, key="num_corners")
    
    corners_data = []
    for i in range(num_corners):
        with st.container():
            st.markdown(f"**コーナー {i+1}**")
            col1, col2 = st.columns([1, 2])
            with col1:
                corner_title = st.text_input(f"コーナー名 {i+1}", key=f"corner_title_{i}", placeholder="例: リスナーの質問箱")
            with col2:
                corner_desc = st.text_area(
                    f"AI解析用説明 {i+1}",
                    key=f"corner_desc_{i}",
                    height=80,
                    placeholder="このコーナーに合うメモの特徴を記述...",
                )
            corners_data.append({"title": corner_title, "description_for_llm": corner_desc})
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("登録", type="primary", use_container_width=True, key="create_program_btn"):
            if new_program_title and new_program_email:
                try:
                    # パーソナリティIDを取得
                    personality_ids = [
                        p['id'] for p in personalities if p['name'] in selected_personalities
                    ]
                    
                    # 番組データを作成
                    program_data = {
                        "title": new_program_title,
                        "email_address": new_program_email,
                        "broadcast_schedule": new_program_schedule,
                        "personality_ids": personality_ids,
                        "corners": [c for c in corners_data if c["title"]],
                    }
                    
                    api_client.create_program(program_data)
                    st.success("番組を登録しました！")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"登録エラー: {e}")
            else:
                st.warning("番組名とメールアドレスは必須です")
    with col2:
        if st.button("キャンセル", use_container_width=True, key="cancel_program_btn"):
            st.rerun()

st.divider()

# 番組一覧
try:
    # フィルタリング
    personality_id = None
    if selected_personality != "全てのパーソナリティ" and personalities:
        # 選択されたパーソナリティのIDを取得
        for p in personalities:
            display_name = f"{p['name']}" + (f" ({p['nickname']})" if p.get('nickname') else "")
            if display_name == selected_personality:
                personality_id = p['id']
                break
    
    programs = api_client.get_programs(
        personality_id=personality_id,
        search=program_search if program_search else None
    )
    
    st.markdown(f"### 登録済み番組 ({len(programs)}件)")
    
    if not programs:
        st.info("番組が登録されていません。新しい番組を登録してください。")
    else:
        for program in programs:
            with st.expander(f"{program['title']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**メールアドレス:** {program.get('email_address', 'N/A')}")
                    st.markdown(f"**放送スケジュール:** {program.get('broadcast_schedule', 'N/A')}")
                    
                    # パーソナリティ表示
                    personality_names = [p['name'] for p in program.get('personalities', [])]
                    if personality_names:
                        st.markdown(f"**パーソナリティ:** {', '.join(personality_names)}")
                
                with col2:
                    if st.button("編集", key=f"edit_program_{program['id']}", use_container_width=True):
                        st.info("編集機能は実装予定です")
                    if st.button("削除", key=f"delete_program_{program['id']}", use_container_width=True):
                        try:
                            api_client.delete_program(program['id'])
                            st.success("番組を削除しました")
                            st.rerun()
                        except Exception as e:
                            st.error(f"削除エラー: {e}")
                
                st.markdown("---")
                st.markdown("#### コーナー一覧")
                
                corners = program.get('corners', [])
                
                if not corners:
                    st.info("コーナーが登録されていません")
                else:
                    for corner in corners:
                        st.markdown(
                            f"""
                            <div class="corner-card">
                                <h4>{corner['title']}</h4>
                                <div class="corner-description">
                                    <strong>AI解析用説明:</strong><br>
                                    {corner['description_for_llm']}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                
                if st.button(f"コーナーを追加", key=f"add_corner_{program['id']}", use_container_width=True):
                    st.info("コーナー追加機能は実装予定です")
except Exception as e:
    st.error(f"番組の取得に失敗: {e}")

# サイドバー
with st.sidebar:
    st.header("統計情報")
    try:
        total_programs = len(api_client.get_programs())
        total_personalities = len(api_client.get_personalities())
        
        st.metric("総番組数", f"{total_programs}件")
        st.metric("パーソナリティ数", f"{total_personalities}名")
    except:
        st.metric("総番組数", "取得失敗")
        st.metric("パーソナリティ数", "取得失敗")
    
    st.divider()
    
    st.header("操作")
    if st.button("ダッシュボードへ", use_container_width=True):
        st.switch_page("app.py")
    if st.button("メモ一覧", use_container_width=True):
        st.switch_page("pages/1_memos.py")
