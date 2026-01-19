"""
カスタムCSSスタイル
"""


def get_custom_css() -> str:
    """カスタムCSSを返す"""
    return """
    <style>
    /* メインカラー */
    :root {
        --primary-color: #2b8cee;
        --background-light: #f6f7f8;
        --background-dark: #101922;
    }
    
    /* 全体のフォント */
    .main {
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
    }
    
    /* カードスタイル */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* 統計カード */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        margin-bottom: 1rem;
    }
    
    .stat-card h3 {
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    
    .stat-card p {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* プライマリボタン */
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        border: none;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #1f7ad9;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(43, 140, 238, 0.3);
    }
    
    /* メモカード */
    .memo-card {
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 0.75rem;
        transition: all 0.2s;
    }
    
    .memo-card:hover {
        border-color: var(--primary-color);
        box-shadow: 0 4px 12px rgba(43, 140, 238, 0.1);
    }
    
    /* バッジ */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-primary {
        background-color: rgba(43, 140, 238, 0.1);
        color: var(--primary-color);
    }
    
    .badge-success {
        background-color: rgba(34, 197, 94, 0.1);
        color: #22c55e;
    }
    
    .badge-warning {
        background-color: rgba(251, 146, 60, 0.1);
        color: #fb923c;
    }
    
    .badge-secondary {
        background-color: rgba(107, 114, 128, 0.1);
        color: #6b7280;
    }
    
    /* アイコン付きテキスト */
    .icon-text {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* セクションヘッダー */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #1f2937;
    }
    
    /* 検索ボックス */
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #d1d5db;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(43, 140, 238, 0.1);
    }
    
    /* セレクトボックス */
    .stSelectbox select {
        border-radius: 8px;
    }
    
    /* テキストエリア */
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #d1d5db;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(43, 140, 238, 0.1);
    }
    
    /* 番組カード */
    .program-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    
    .program-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .program-icon {
        width: 48px;
        height: 48px;
        border-radius: 8px;
        background: linear-gradient(135deg, #f97316 0%, #dc2626 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    /* コーナーカード */
    .corner-card {
        background: #f9fafb;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 0.5rem;
    }
    
    .corner-card h4 {
        font-size: 0.875rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1f2937;
    }
    
    .corner-description {
        font-size: 0.75rem;
        color: #6b7280;
        background: white;
        padding: 0.5rem;
        border-radius: 4px;
        border: 1px solid #e5e7eb;
    }
    
    /* Streamlitのデフォルトパディング調整 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* サイドバー */
    [data-testid="stSidebar"] {
        background-color: #f9fafb;
    }
    
    /* ステータスバッジ */
    .status-draft {
        background-color: rgba(107, 114, 128, 0.1);
        color: #6b7280;
    }
    
    .status-sent {
        background-color: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
    }
    
    .status-accepted {
        background-color: rgba(34, 197, 94, 0.1);
        color: #22c55e;
    }
    
    .status-rejected {
        background-color: rgba(239, 68, 68, 0.1);
        color: #ef4444;
    }
    </style>
    """
