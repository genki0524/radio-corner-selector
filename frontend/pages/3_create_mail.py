import streamlit as st
import sys
from pathlib import Path
import urllib.parse

from utils.api_client import api_client
from utils.styles import get_custom_css

sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="メール作成",
    layout="centered",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("メール作成・投稿設定")

# セッション状態の初期化
if "selected_memo_id" not in st.session_state:
    st.session_state["selected_memo_id"] = None
if "selected_corner_id" not in st.session_state:
    st.session_state["selected_corner_id"] = None
if "mail_subject" not in st.session_state:
    st.session_state["mail_subject"] = ""
if "mail_body" not in st.session_state:
    st.session_state["mail_body"] = ""

# メモ選択
st.subheader("元ネタのメモを選択")
try:
    memos = api_client.get_memos()
    memo_options = ["メモを選択してください"] + [f"ID:{m['id']} - {m['content'][:50]}..." for m in memos]
    selected_memo_option = st.selectbox("メモ", memo_options, key="select_memo")
    
    selected_memo = None
    if selected_memo_option != "メモを選択してください":
        memo_id = int(selected_memo_option.split(":")[1].split(" ")[0])
        selected_memo = api_client.get_memo(memo_id)
except Exception as e:
    st.error(f"メモの取得に失敗: {e}")
    selected_memo = None

st.divider()

# AIによるコーナー推奨
if selected_memo:
    st.subheader("AI解析による推奨コーナー")
    
    try:
        # LLM解析を実行
        analysis_result = api_client.analyze_memo(selected_memo['id'])
        recommendations = analysis_result.get('recommendations', [])
        
        if recommendations:
            recommended_corner = recommendations[0]  # 最も推奨度の高いもの
            
            col1, col2 = st.columns([3, 1])
            with col1:
                score_percent = int(recommended_corner['score'] * 100)
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, rgba(43, 140, 238, 0.1) 0%, rgba(43, 140, 238, 0.2) 100%); 
                                border: 2px solid #2b8cee; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                            <span style="font-size: 1.5rem;">⭐</span>
                            <span style="color: #2b8cee; font-weight: 700; font-size: 0.875rem;">AI推奨コーナー</span>
                            <span class="badge badge-primary">一致度: {score_percent}%</span>
                        </div>
                        <h3 style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem; color: #1f2937;">
                            {recommended_corner['corner_title']}
                        </h3>
                        <p style="color: #6b7280; margin-bottom: 0.5rem;">番組: {recommended_corner['program_title']}</p>
                        <p style="color: #6b7280; font-size: 0.875rem;">
                            推奨理由: {recommended_corner['reason']}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col2:
                st.write("")
                st.write("")
                if st.button("このコーナーに投稿", type="primary", use_container_width=True, key="use_recommended"):
                    st.session_state["selected_corner_id"] = recommended_corner['corner_id']
                    st.session_state["selected_program_id"] = recommended_corner['program_id']
                    st.success("コーナーを選択しました！")
        else:
            st.info("推奨コーナーが見つかりませんでした")
    except Exception as e:
        st.warning(f"AI解析に失敗しました: {e}\n手動でコーナーを選択してください。")

st.divider()

# 手動でコーナーを選択
st.subheader("コーナーを手動で選択")

try:
    programs = api_client.get_programs()
    program_titles = ["番組を選択してください"] + [p['title'] for p in programs]
    selected_program_title = st.selectbox("番組", program_titles, key="select_program")
    
    if selected_program_title != "番組を選択してください":
        selected_program = next((p for p in programs if p['title'] == selected_program_title), None)
        if selected_program:
            st.session_state["selected_program_id"] = selected_program['id']
            corners = selected_program.get('corners', [])
            corner_titles = ["コーナーを選択してください"] + [c['title'] for c in corners]
            selected_corner_title = st.selectbox("コーナー", corner_titles, key="select_corner")
            
            if selected_corner_title != "コーナーを選択してください":
                selected_corner = next((c for c in corners if c['title'] == selected_corner_title), None)
                if selected_corner:
                    st.session_state["selected_corner_id"] = selected_corner['id']
except Exception as e:
    st.error(f"番組の取得に失敗: {e}")

st.divider()

# 現在の選択状態を表示
if st.session_state.get("selected_program_id"):
    try:
        programs = api_client.get_programs()
        current_program = next((p for p in programs if p['id'] == st.session_state["selected_program_id"]), None)
        if current_program:
            current_corner = next((c for c in current_program.get('corners', []) if c['id'] == st.session_state["selected_corner_id"]), None)
            if current_corner:
                st.success(f"投稿先: {current_program['title']} - {current_corner['title']} ({current_program.get('email_address', 'N/A')})")
            else:
                st.success(f"投稿先: {current_program['title']})")
    except Exception as e:
        pass

st.divider()

# メール作成
st.subheader("メール内容")

col1, col2 = st.columns([3, 1])

with col1:
    # プロフィール選択
    try:
        profiles = api_client.get_profiles()
        profile_options = [p['name'] for p in profiles]
        if profile_options:
            selected_profile_name = st.selectbox("使用するプロフィール", profile_options, key="select_profile")
            selected_profile = next((p for p in profiles if p['name'] == selected_profile_name), None)
        else:
            st.warning("プロフィールが登録されていません")
            selected_profile = None
    except Exception as e:
        st.error(f"プロフィールの取得に失敗: {e}")
        selected_profile = None

with col2:
    if st.button("プロフィール管理", use_container_width=True):
        st.switch_page("pages/4_profiles.py")

# メール件名
mail_subject = st.text_input(
    "件名",
    value=st.session_state.get("mail_subject", ""),
)
st.session_state["mail_subject"] = mail_subject

mail_body = st.text_area(
    "本文",
    value=st.session_state.get("mail_body"),
    height=300,
    placeholder="メール本文を入力してください...",
)
st.session_state["mail_body"] = mail_body

st.divider()

# アクション
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("下書き保存", type="secondary", use_container_width=True, key="save_draft"):
        # if st.session_state.get("selected_corner_id") and mail_subject and mail_body:
        if mail_subject and mail_body:
            try:
                mail_data = {
                    "corner_id": st.session_state.get("selected_corner_id"),
                    "memo_id": selected_memo['id'] if selected_memo else None,
                    "subject": mail_subject,
                    "body": mail_body,
                    "status": "下書き",
                }

                api_client.create_mail(mail_data)
                st.success("下書きを保存しました")
            except Exception as e:
                st.error(f"保存エラー: {e}")
        else:
            st.warning("コーナー、件名、本文を入力してください")

with col2:
    if st.button("メーラーで開く", type="primary", use_container_width=True, key="open_mailer"):
        if st.session_state.get("selected_program_id") and st.session_state.get("selected_corner_id") and mail_subject and mail_body:
            try:
                programs = api_client.get_programs()
                current_program = next((p for p in programs if p['id'] == st.session_state["selected_program_id"]), None)
                
                mail_data = {
                    "corner_id": st.session_state.get("selected_corner_id"),
                    "memo_id": selected_memo['id'] if selected_memo else None,
                    "subject": mail_subject,
                    "body": mail_body,
                    "status": "送信済み",
                }
                api_client.create_mail(mail_data)

                if current_program:
                    email_address = current_program.get('email_address', '')
                    mailto_link = f"mailto:{email_address}?subject={urllib.parse.quote(mail_subject)}&body={urllib.parse.quote(mail_body)}"
                    st.markdown(f"[メーラーを起動]({mailto_link})")
                    st.success("メーラーを起動します")
                else:
                    st.error("番組情報の取得に失敗しました")
            except Exception as e:
                st.error(f"エラー: {e}")
        else:
            st.warning("番組とコーナーを選択し、件名と本文を入力してください")

with col3:
    if st.button("リセット", use_container_width=True):
        st.session_state["mail_subject"] = ""
        st.session_state["mail_body"] = ""
        st.rerun()

with col4:
    if st.button("キャンセル", use_container_width=True):
        st.switch_page("app.py")
