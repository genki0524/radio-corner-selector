"""
モックデータモジュール
バックエンドAPI実装前のフロントエンド開発用
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any


# ユーザー
MOCK_USER = {
    "id": 1,
    "email": "user@example.com",
}

# プロフィール
MOCK_PROFILES = [
    {
        "id": 1,
        "user_id": 1,
        "name": "メインプロフィール",
        "radio_name": "ラジオネーム太郎",
        "real_name": "山田太郎",
        "address": "東京都渋谷区",
        "phone": "090-1234-5678",
    },
    {
        "id": 2,
        "user_id": 1,
        "name": "サブプロフィール",
        "radio_name": "匿名希望",
        "real_name": "",
        "address": "",
        "phone": "",
    },
]

# パーソナリティ
MOCK_PERSONALITIES = [
    {"id": 1, "user_id": 1, "name": "佐藤健太", "nickname": "けんちゃん"},
    {"id": 2, "user_id": 1, "name": "鈴木エミ", "nickname": "えみりん"},
    {"id": 3, "user_id": 1, "name": "田中光", "nickname": None},
    {"id": 4, "user_id": 1, "name": "星野美咲", "nickname": "みーちゃん"},
]

# 番組
MOCK_PROGRAMS = [
    {
        "id": 1,
        "user_id": 1,
        "title": "モーニング・ロースト",
        "email_address": "morning@radio.com",
        "broadcast_schedule": "月〜金 6:00-10:00",
        "default_profile_id": 1,
        "personalities": [1, 2],  # personality_ids
    },
    {
        "id": 2,
        "user_id": 1,
        "title": "レイトナイト・ジャズ",
        "email_address": "jazz@radio.com",
        "broadcast_schedule": "金 22:00-24:00",
        "default_profile_id": 2,
        "personalities": [3],
    },
    {
        "id": 3,
        "user_id": 1,
        "title": "週末トーク",
        "email_address": "weekend@radio.com",
        "broadcast_schedule": "土日 15:00-17:00",
        "default_profile_id": 1,
        "personalities": [2, 4],
    },
]

# コーナー
MOCK_CORNERS = [
    {
        "id": 1,
        "program_id": 1,
        "title": "街角スポットライト",
        "description_for_llm": "地域の人々や店舗を紹介するコーナー。人間味のあるエピソードや、地域に根ざした活動について。",
    },
    {
        "id": 2,
        "program_id": 1,
        "title": "朝のニュース解説",
        "description_for_llm": "時事ニュースをわかりやすく解説。政治、経済、社会問題など。",
    },
    {
        "id": 3,
        "program_id": 1,
        "title": "リスナーの質問箱",
        "description_for_llm": "リスナーからの質問に答えるコーナー。日常の疑問、悩み相談など。",
    },
    {
        "id": 4,
        "program_id": 1,
        "title": "今日の一曲",
        "description_for_llm": "音楽リクエストコーナー。思い出の曲、おすすめの曲の紹介。",
    },
    {
        "id": 5,
        "program_id": 2,
        "title": "ジャズの歴史",
        "description_for_llm": "ジャズの歴史やアーティストについて深掘り。名盤紹介など。",
    },
    {
        "id": 6,
        "program_id": 2,
        "title": "深夜の雑談",
        "description_for_llm": "リラックスした雰囲気での自由な雑談。日常のふとした気づきなど。",
    },
    {
        "id": 7,
        "program_id": 3,
        "title": "週末のおでかけ情報",
        "description_for_llm": "イベント情報、観光スポット、グルメ情報など。",
    },
]

# メモ
MOCK_MEMOS = [
    {
        "id": 1,
        "user_id": 1,
        "content": "駅前の喫茶店のマスターに話を聞いた。40年もお店を続けているらしい。80年代のジャズシーンの話がとても興味深かった。常連さんとの交流についても語ってくれた。",
        "created_at": datetime.now() - timedelta(hours=2),
    },
    {
        "id": 2,
        "user_id": 1,
        "content": "来週月曜からメインストリートで新しい工事が始まる。午前8時から10時の間は激しい渋滞が予想される。通勤ルートの変更を検討したほうがいい。",
        "created_at": datetime.now() - timedelta(hours=5),
    },
    {
        "id": 3,
        "user_id": 1,
        "content": "高校サッカーの試合結果。中央高校が2-1で西高校に勝利。後半終了間際の劇的な逆転ゴールだった。地元出身の選手が決めたらしい。",
        "created_at": datetime.now() - timedelta(days=1),
    },
    {
        "id": 4,
        "user_id": 1,
        "content": "気象庁から盆地エリアにフラッシュフラッドの警戒が出ている。屋外インタビューを屋内に変更すべきか検討が必要。",
        "created_at": datetime.now() - timedelta(days=2),
    },
    {
        "id": 5,
        "user_id": 1,
        "content": "新しいカフェがオープン。オーガニックコーヒーと手作りケーキが人気。店主は元パティシエでフランス修行の経験あり。",
        "created_at": datetime.now() - timedelta(days=3),
    },
]

# メール
MOCK_MAILS = [
    {
        "id": 1,
        "corner_id": 1,
        "memo_id": 1,
        "subject": "街角スポットライト：駅前喫茶店の話",
        "body": "いつも番組を楽しく聴いています。\n\n駅前の喫茶店「珈琲の時間」のマスターに取材してきました...",
        "status": "下書き",
        "sent_at": None,
        "created_at": datetime.now() - timedelta(hours=1),
        "updated_at": datetime.now() - timedelta(hours=1),
    },
    {
        "id": 2,
        "corner_id": 4,
        "memo_id": None,
        "subject": "今日の一曲リクエスト",
        "body": "ラジオネーム太郎です。\n\n思い出の曲をリクエストさせてください...",
        "status": "送信済み",
        "sent_at": datetime.now() - timedelta(days=5),
        "created_at": datetime.now() - timedelta(days=5),
        "updated_at": datetime.now() - timedelta(days=5),
    },
    {
        "id": 3,
        "corner_id": 3,
        "memo_id": None,
        "subject": "質問：コーヒーの淹れ方について",
        "body": "いつも楽しく聴いています。\n\n美味しいコーヒーの淹れ方を教えてください...",
        "status": "採用",
        "sent_at": datetime.now() - timedelta(days=10),
        "created_at": datetime.now() - timedelta(days=10),
        "updated_at": datetime.now() - timedelta(days=8),
    },
]


def get_programs() -> List[Dict[str, Any]]:
    """番組一覧を取得"""
    return MOCK_PROGRAMS.copy()


def get_program_by_id(program_id: int) -> Dict[str, Any] | None:
    """番組をIDで取得"""
    for program in MOCK_PROGRAMS:
        if program["id"] == program_id:
            return program.copy()
    return None


def get_corners_by_program_id(program_id: int) -> List[Dict[str, Any]]:
    """番組のコーナー一覧を取得"""
    return [c.copy() for c in MOCK_CORNERS if c["program_id"] == program_id]


def get_personalities() -> List[Dict[str, Any]]:
    """パーソナリティ一覧を取得"""
    return MOCK_PERSONALITIES.copy()


def get_personality_by_id(personality_id: int) -> Dict[str, Any] | None:
    """パーソナリティをIDで取得"""
    for p in MOCK_PERSONALITIES:
        if p["id"] == personality_id:
            return p.copy()
    return None


def get_memos() -> List[Dict[str, Any]]:
    """メモ一覧を取得"""
    return MOCK_MEMOS.copy()


def get_memo_by_id(memo_id: int) -> Dict[str, Any] | None:
    """メモをIDで取得"""
    for memo in MOCK_MEMOS:
        if memo["id"] == memo_id:
            return memo.copy()
    return None


def get_mails() -> List[Dict[str, Any]]:
    """メール一覧を取得"""
    return MOCK_MAILS.copy()


def get_profiles() -> List[Dict[str, Any]]:
    """プロフィール一覧を取得"""
    return MOCK_PROFILES.copy()


def get_profile_by_id(profile_id: int) -> Dict[str, Any] | None:
    """プロフィールをIDで取得"""
    for profile in MOCK_PROFILES:
        if profile["id"] == profile_id:
            return profile.copy()
    return None


def get_mail_stats() -> Dict[str, int]:
    """メール統計を取得"""
    mails = get_mails()
    return {
        "下書き": len([m for m in mails if m["status"] == "下書き"]),
        "送信済み": len([m for m in mails if m["status"] == "送信済み"]),
        "採用": len([m for m in mails if m["status"] == "採用"]),
        "不採用": len([m for m in mails if m["status"] == "不採用"]),
    }
