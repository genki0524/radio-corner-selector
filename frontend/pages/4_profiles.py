"""
プロフィール設定ページ
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import api_client
from utils.styles import get_custom_css

st.set_page_config(
    page_title="プロフィール設定",
    page_icon="👥",
    layout="wide",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("プロフィール設定")
st.markdown("番組投稿時に使用するプロフィール（署名）を管理します")

st.divider()

# 新規プロフィール作成
with st.expander("新しいプロフィールを作成", expanded=False):
    st.markdown("#### プロフィール情報")
    
    new_profile_name = st.text_input("管理用名称", placeholder="例: メインプロフィール", key="new_profile_name")
    new_profile_radio_name = st.text_input("ラジオネーム", placeholder="例: ラジオネーム太郎", key="new_profile_radio_name")
    
    col1, col2 = st.columns(2)
    with col1:
        new_profile_real_name = st.text_input("本名 (任意)", placeholder="例: 山田太郎", key="new_profile_real_name")
        new_profile_phone = st.text_input("電話番号 (任意)", placeholder="例: 090-1234-5678", key="new_profile_phone")
    with col2:
        new_profile_address = st.text_input("住所 (任意)", placeholder="例: 東京都渋谷区", key="new_profile_address")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("保存", type="primary", use_container_width=True, key="save_profile"):
            if new_profile_name and new_profile_radio_name:
                try:
                    profile_data = {
                        "name": new_profile_name,
                        "radio_name": new_profile_radio_name,
                        "real_name": new_profile_real_name or None,
                        "address": new_profile_address or None,
                        "phone": new_profile_phone or None,
                    }
                    api_client.create_profile(profile_data)
                    st.success("プロフィールを保存しました！")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"保存エラー: {e}")
            else:
                st.warning("管理用名称とラジオネームは必須です")
    with col2:
        if st.button("キャンセル", use_container_width=True, key="cancel_profile"):
            st.rerun()

st.divider()

# プロフィール一覧
try:
    profiles = api_client.get_profiles()
    
    st.markdown(f"### 登録済みプロフィール ({len(profiles)}件)")
    
    if not profiles:
        st.info("プロフィールが登録されていません。新しいプロフィールを作成してください。")
    else:
        for profile in profiles:
            with st.expander(f"{profile['name']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(
                        f"""
                        <div class="card">
                            <h4 style="color: #2b8cee; font-size: 1.1rem; margin-bottom: 1rem;">
                                {profile['name']}
                            </h4>
                            
                            <div style="margin-bottom: 0.75rem;">
                                <strong style="color: #6b7280; font-size: 0.875rem;">ラジオネーム:</strong>
                                <p style="color: #1f2937; margin: 0.25rem 0 0 0;">{profile['radio_name']}</p>
                            </div>
                            
                            {f'''
                            <div style="margin-bottom: 0.75rem;">
                                <strong style="color: #6b7280; font-size: 0.875rem;">本名:</strong>
                                <p style="color: #1f2937; margin: 0.25rem 0 0 0;">{profile['real_name']}</p>
                            </div>
                            ''' if profile.get('real_name') else ''}
                            
                            {f'''
                            <div style="margin-bottom: 0.75rem;">
                                <strong style="color: #6b7280; font-size: 0.875rem;">住所:</strong>
                                <p style="color: #1f2937; margin: 0.25rem 0 0 0;">{profile['address']}</p>
                            </div>
                            ''' if profile.get('address') else ''}
                            
                            {f'''
                            <div style="margin-bottom: 0.75rem;">
                                <strong style="color: #6b7280; font-size: 0.875rem;">電話番号:</strong>
                                <p style="color: #1f2937; margin: 0.25rem 0 0 0;">{profile['phone']}</p>
                            </div>
                            ''' if profile.get('phone') else ''}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("編集", key=f"edit_profile_{profile['id']}", use_container_width=True):
                        st.info("編集機能は実装予定です")
                    if st.button("削除", key=f"delete_profile_{profile['id']}", use_container_width=True):
                        try:
                            api_client.delete_profile(profile['id'])
                            st.success("プロフィールを削除しました")
                            st.rerun()
                        except Exception as e:
                            st.error(f"削除エラー: {e}")
                
                st.markdown("---")
                
                # プレビュー
                st.markdown("#### メール署名プレビュー")
                signature = f"""ラジオネーム: {profile['radio_name']}"""
                if profile.get('real_name'):
                    signature += f"\n本名: {profile['real_name']}"
                if profile.get('address'):
                    signature += f"\n住所: {profile['address']}"
                if profile.get('phone'):
                    signature += f"\n電話番号: {profile['phone']}"
                
                st.code(signature, language=None)
except Exception as e:
    st.error(f"プロフィールの取得に失敗: {e}")

# サイドバー
with st.sidebar:
    st.header("統計情報")
    try:
        total_profiles = len(api_client.get_profiles())
        st.metric("総プロフィール数", f"{total_profiles}件")
    except:
        st.metric("総プロフィール数", "取得失敗")
    
    st.divider()
    
    st.header("ヒント")
    st.markdown("""
    **プロフィールの使い分け:**
    - 番組ごとに異なるプロフィールを使用できます
    - 匿名で投稿したい場合は本名を空欄に
    - 複数のラジオネームを使い分けることも可能
    """)
    
    st.divider()
    
    st.header("操作")
    if st.button("ダッシュボードへ", use_container_width=True):
        st.switch_page("app.py")
    if st.button("メール作成", use_container_width=True, type="primary"):
        st.switch_page("pages/3_mail.py")
