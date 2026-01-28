import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

from utils.api_client import api_client
from utils.styles import get_custom_css

sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="送信済みメール一覧",
    layout="centered",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("送信済みメール一覧")

# 検索・フィルター
col1, col2 = st.columns([3, 1])
with col1:
    search_query = st.text_input("メールを検索", placeholder="件名や本文でキーワード検索...")
with col2:
    status_filter = st.selectbox(
        "ステータス",
        ["すべて","送信済み", "採用", "不採用"],
    )

st.divider()

# メール一覧
try:
    # ステータスフィルター適用
    filter_value = None if status_filter == "すべて" else status_filter
    mails = api_client.get_mails(status_filter=filter_value)
    
    # 検索フィルタリング
    if search_query:
        mails = [
            m for m in mails 
            if search_query.lower() in m["subject"].lower() 
            or search_query.lower() in m["body"].lower()
        ]
    
    st.markdown(f"### メール一覧 ({len(mails)}件)")
    
    if not mails:
        st.info("メールがありません。")
    else:
        # 番組とコーナー情報を取得
        programs = api_client.get_programs()
        
        for mail in mails:
            with st.container():
                # ステータスに応じたバッジの色を設定
                status_colors = {
                    "下書き": "#9ca3af",
                    "送信済み": "#2b8cee",
                    "採用": "#34d399",
                    "不採用": "#6b7280",
                }
                badge_color = status_colors.get(mail['status'], "#9ca3af")
                
                # 送信日時または作成日時を表示
                if mail.get('sent_at'):
                    display_date = datetime.fromisoformat(str(mail['sent_at']).replace('Z', '+00:00'))
                    date_label = "送信日時"
                else:
                    display_date = datetime.fromisoformat(str(mail['created_at']).replace('Z', '+00:00'))
                    date_label = "作成日時"
                
                # コーナー情報を取得
                corner_info = ""
                if mail.get('corner_id'):
                    for program in programs:
                        corners = program.get('corners', [])
                        corner = next((c for c in corners if c['id'] == mail['corner_id']), None)
                        if corner:
                            corner_info = f"{program['title']} - {corner['title']}"
                            break
                else:
                    corner_info = program['title']
                
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    st.markdown(
                        f"""
                        <div style="background-color: white; border-radius: 12px; padding: 1.5rem; 
                                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); margin-bottom: 1rem; 
                                    cursor: pointer; transition: all 0.2s;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                                <div style="display: flex; gap: 0.5rem; align-items: center;">
                                    <span style="background-color: {badge_color}; color: white; padding: 0.25rem 0.75rem; 
                                                border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">
                                        {mail['status']}
                                    </span>
                                    <span style="color: #9ca3af; font-size: 0.75rem;">ID: {mail['id']}</span>
                                </div>
                                <span style="color: #9ca3af; font-size: 0.75rem;">
                                    {date_label}: {display_date.strftime('%Y/%m/%d %H:%M')}
                                </span>
                            </div>
                            {f'<div style="color: #2b8cee; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem;">📻 {corner_info}</div>' if corner_info else ''}
                            <h3 style="color: #1f2937; font-weight: 700; font-size: 1.125rem; margin-bottom: 0.5rem;">
                                {mail['subject']}
                            </h3>
                            <p style="color: #6b7280; font-size: 0.875rem; line-height: 1.5; 
                                      overflow: hidden; text-overflow: ellipsis; display: -webkit-box; 
                                      -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                                {mail['body'][:100]}...
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("詳細", key=f"detail_{mail['id']}", use_container_width=True, type="primary"):
                        st.session_state["selected_mail_id"] = mail["id"]
                        st.session_state["show_mail_modal"] = True

except Exception as e:
    st.error(f"メールの取得に失敗: {e}")

# メール詳細モーダル
if st.session_state.get("show_mail_modal", False) and st.session_state.get("selected_mail_id"):
    selected_mail_id = st.session_state["selected_mail_id"]
    
    try:
        # 選択されたメールを取得
        mails = api_client.get_mails()
        selected_mail = next((m for m in mails if m["id"] == selected_mail_id), None)
        
        if selected_mail:
            # モーダル風のダイアログを表示
            @st.dialog("メール詳細", width="large")
            def show_mail_detail():
                # 日時表示
                if selected_mail.get('sent_at'):
                    display_date = datetime.fromisoformat(str(selected_mail['sent_at']).replace('Z', '+00:00'))
                    date_label = "送信日時"
                else:
                    display_date = datetime.fromisoformat(str(selected_mail['created_at']).replace('Z', '+00:00'))
                    date_label = "作成日時"
                
                # ステータスバッジ
                status_colors = {
                    "下書き": "#9ca3af",
                    "送信済み": "#2b8cee",
                    "採用": "#34d399",
                    "不採用": "#6b7280",
                }
                badge_color = status_colors.get(selected_mail['status'], "#9ca3af")
                
                # コーナー情報を取得
                corner_info = ""
                program_title = ""
                corner_title = ""
                if selected_mail.get('corner_id'):
                    programs = api_client.get_programs()
                    for program in programs:
                        corners = program.get('corners', [])
                        corner = next((c for c in corners if c['id'] == selected_mail['corner_id']), None)
                        if corner:
                            program_title = program['title']
                            corner_title = corner['title']
                            corner_info = f"<div style='background: linear-gradient(135deg, rgba(43, 140, 238, 0.1) 0%, rgba(43, 140, 238, 0.15) 100%); border-radius: 8px; padding: 1rem; margin-bottom: 1rem;'><div style='color: #2b8cee; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.25rem;'>投稿先コーナー</div><div style='color: #1f2937; font-weight: 700;'>📻 {program_title} - {corner_title}</div></div>"
                            break
                
                # メール情報表示
                st.markdown(
                    f"""
                    <div style="margin-bottom: 1.5rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                            <span style="background-color: {badge_color}; color: white; padding: 0.5rem 1rem; 
                                        border-radius: 9999px; font-size: 0.875rem; font-weight: 600;">
                                {selected_mail['status']}
                            </span>
                            <span style="color: #6b7280; font-size: 0.875rem;">
                                {date_label}: {display_date.strftime('%Y/%m/%d %H:%M')}
                            </span>
                        </div>
                        {corner_info}
                        <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.5rem;">
                            メールID: {selected_mail['id']}
                        </div>
                        {f'<div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 1rem;">元ネタメモID: {selected_mail["memo_id"]}</div>' if selected_mail.get('memo_id') else ''}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                st.markdown("### 件名")
                st.markdown(f"**{selected_mail['subject']}**")
                
                st.divider()
                
                # 編集モードの管理
                edit_mode_key = f"edit_mode_{selected_mail['id']}"
                if edit_mode_key not in st.session_state:
                    st.session_state[edit_mode_key] = False
                
                # 件名と本文の編集
                col_header1, col_header2 = st.columns([3, 1])
                with col_header1:
                    st.markdown("### 本文")
                with col_header2:
                    st.write("")
                    if not st.session_state[edit_mode_key]:
                        if st.button("編集", key=f"enable_edit_{selected_mail['id']}", use_container_width=True):
                            st.session_state[edit_mode_key] = True
                            st.rerun()
                    else:
                        if st.button("キャンセル", key=f"cancel_edit_{selected_mail['id']}", use_container_width=True):
                            st.session_state[edit_mode_key] = False
                            st.rerun()
                
                # 編集モードに応じて入力フィールドを表示
                if st.session_state[edit_mode_key]:
                    edited_subject = st.text_input(
                        "件名",
                        value=selected_mail['subject'],
                        key=f"edit_subject_{selected_mail['id']}"
                    )
                    edited_body = st.text_area(
                        label="本文",
                        value=selected_mail['body'],
                        height=300,
                        disabled=False,
                        label_visibility="collapsed",
                        key=f"edit_body_{selected_mail['id']}"
                    )
                    
                    # 保存ボタン
                    if st.button("保存", type="primary", use_container_width=True, key=f"save_edit_{selected_mail['id']}"):
                        try:
                            update_data = {
                                "subject": edited_subject,
                                "body": edited_body
                            }
                            api_client.update_mail(selected_mail['id'], update_data)
                            st.success("メールを更新しました")
                            st.session_state[edit_mode_key] = False
                            st.session_state["show_mail_modal"] = False
                            st.session_state["selected_mail_id"] = None
                            st.rerun()
                        except Exception as e:
                            st.error(f"メール更新に失敗: {e}")
                else:
                    st.text_area(
                        label="本文",
                        value=selected_mail['body'],
                        height=300,
                        disabled=True,
                        label_visibility="collapsed"
                    )
                
                st.divider()
                
                # ステータス変更
                st.markdown("### ステータス変更")
                col_status1, col_status2 = st.columns(2)
                with col_status1:
                    new_status = st.selectbox(
                        "新しいステータス",
                        ["下書き", "送信済み", "採用", "不採用"],
                        index=["下書き", "送信済み", "採用", "不採用"].index(selected_mail['status']),
                        key=f"status_select_{selected_mail['id']}"
                    )
                with col_status2:
                    st.write("")
                    st.write("")
                    if st.button("ステータス更新", type="secondary", use_container_width=True, key=f"update_status_{selected_mail['id']}"):
                        try:
                            update_data = {"status": new_status}
                            api_client.update_mail(selected_mail['id'], update_data)
                            st.success(f"ステータスを「{new_status}」に更新しました")
                            st.session_state["show_mail_modal"] = False
                            st.session_state["selected_mail_id"] = None
                            st.rerun()
                        except Exception as e:
                            st.error(f"ステータス更新に失敗: {e}")
                
                st.divider()
                
                # 閉じるボタン
                if st.button("閉じる", type="primary", use_container_width=True):
                    st.session_state["show_mail_modal"] = False
                    st.session_state["selected_mail_id"] = None
                    # 編集モードをリセット
                    if edit_mode_key in st.session_state:
                        del st.session_state[edit_mode_key]
                    st.rerun()
            
            show_mail_detail()
    
    except Exception as e:
        st.error(f"メール詳細の取得に失敗: {e}")
        st.session_state["show_mail_modal"] = False
        st.session_state["selected_mail_id"] = None
