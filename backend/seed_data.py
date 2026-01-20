"""
初期データ投入スクリプト
テスト用のサンプルデータをデータベースに投入
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from database import SessionLocal, init_db
from models import (
    User,
    Profile,
    Personality,
    Program,
    Corner,
    Memo,
    Mail,
)


def seed_data(clear_existing: bool = False):
    """初期データを投入
    
    Args:
        clear_existing: 既存データをクリアするかどうか（デフォルト: False）
    """
    db: Session = SessionLocal()
    
    try:
        # データベース初期化
        init_db()
        
        # 既存データのクリア（オプション）
        if clear_existing:
            db.query(Mail).delete()
            db.query(Memo).delete()
            db.query(Corner).delete()
            db.query(Program).delete()
            db.query(Personality).delete()
            db.query(Profile).delete()
            db.query(User).delete()
            db.commit()
            print("🗑️  既存データをクリアしました")
        else:
            # データが既に存在するか確認
            user_count = db.query(User).count()
            if user_count > 0:
                print("ℹ️  既にデータが存在します。処理をスキップします。")
                return
        
        # ユーザー作成
        user = User(
            email="user@example.com",
            password_hash="hashed_password_here"  # 実際はハッシュ化する
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ ユーザー作成: {user.email}")
        
        # プロフィール作成
        profiles = [
            Profile(
                user_id=user.id,
                name="メインプロフィール",
                radio_name="ラジオネーム太郎",
                real_name="山田太郎",
                address="東京都渋谷区",
                phone="090-1234-5678",
            ),
            Profile(
                user_id=user.id,
                name="サブプロフィール",
                radio_name="匿名希望",
                real_name="",
                address="",
                phone="",
            ),
        ]
        for profile in profiles:
            db.add(profile)
        db.commit()
        print(f"✅ プロフィール作成: {len(profiles)}件")
        
        # パーソナリティ作成
        personalities = [
            Personality(user_id=user.id, name="佐藤健太", nickname="けんちゃん"),
            Personality(user_id=user.id, name="鈴木エミ", nickname="えみりん"),
            Personality(user_id=user.id, name="田中光", nickname=None),
            Personality(user_id=user.id, name="星野美咲", nickname="みーちゃん"),
        ]
        for personality in personalities:
            db.add(personality)
        db.commit()
        print(f"✅ パーソナリティ作成: {len(personalities)}件")
        
        # 番組作成
        program1 = Program(
            user_id=user.id,
            default_profile_id=profiles[0].id,
            title="モーニング・ロースト",
            email_address="morning@radio.com",
            broadcast_schedule="月〜金 6:00-10:00",
        )
        program1.personalities = [personalities[0], personalities[1]]
        db.add(program1)
        db.commit()
        db.refresh(program1)
        
        program2 = Program(
            user_id=user.id,
            default_profile_id=profiles[1].id,
            title="レイトナイト・ジャズ",
            email_address="jazz@radio.com",
            broadcast_schedule="金 22:00-24:00",
        )
        program2.personalities = [personalities[2]]
        db.add(program2)
        db.commit()
        db.refresh(program2)
        
        program3 = Program(
            user_id=user.id,
            default_profile_id=profiles[0].id,
            title="週末トーク",
            email_address="weekend@radio.com",
            broadcast_schedule="土日 15:00-17:00",
        )
        program3.personalities = [personalities[1], personalities[3]]
        db.add(program3)
        db.commit()
        db.refresh(program3)
        
        print(f"✅ 番組作成: 3件")
        
        # コーナー作成
        corners = [
            Corner(
                program_id=program1.id,
                title="街角スポットライト",
                description_for_llm="地域の人々や店舗を紹介するコーナー。人間味のあるエピソードや、地域に根ざした活動について。",
            ),
            Corner(
                program_id=program1.id,
                title="朝のニュース解説",
                description_for_llm="時事ニュースをわかりやすく解説。政治、経済、社会問題など。",
            ),
            Corner(
                program_id=program1.id,
                title="リスナーの質問箱",
                description_for_llm="リスナーからの質問に答えるコーナー。日常の疑問、悩み相談など。",
            ),
            Corner(
                program_id=program1.id,
                title="今日の一曲",
                description_for_llm="音楽リクエストコーナー。思い出の曲、おすすめの曲の紹介。",
            ),
            Corner(
                program_id=program2.id,
                title="ジャズの歴史",
                description_for_llm="ジャズの歴史やアーティストについて深掘り。名盤紹介など。",
            ),
            Corner(
                program_id=program2.id,
                title="深夜の雑談",
                description_for_llm="リラックスした雰囲気での自由な雑談。日常のふとした気づきなど。",
            ),
            Corner(
                program_id=program3.id,
                title="週末のおでかけ情報",
                description_for_llm="イベント情報、観光スポット、グルメ情報など。",
            ),
        ]
        for corner in corners:
            db.add(corner)
        db.commit()
        print(f"✅ コーナー作成: {len(corners)}件")
        
        # メモ作成
        memos = [
            Memo(
                user_id=user.id,
                content="駅前の喫茶店のマスターに話を聞いた。40年もお店を続けているらしい。80年代のジャズシーンの話がとても興味深かった。常連さんとの交流についても語ってくれた。",
                created_at=datetime.now() - timedelta(hours=2),
            ),
            Memo(
                user_id=user.id,
                content="来週月曜からメインストリートで新しい工事が始まる。午前8時から10時の間は激しい渋滞が予想される。通勤ルートの変更を検討したほうがいい。",
                created_at=datetime.now() - timedelta(hours=5),
            ),
            Memo(
                user_id=user.id,
                content="高校サッカーの試合結果。中央高校が2-1で西高校に勝利。後半終了間際の劇的な逆転ゴールだった。地元出身の選手が決めたらしい。",
                created_at=datetime.now() - timedelta(days=1),
            ),
            Memo(
                user_id=user.id,
                content="気象庁から盆地エリアにフラッシュフラッドの警戒が出ている。屋外インタビューを屋内に変更すべきか検討が必要。",
                created_at=datetime.now() - timedelta(days=2),
            ),
            Memo(
                user_id=user.id,
                content="新しいカフェがオープン。オーガニックコーヒーと手作りケーキが人気。店主は元パティシエでフランス修行の経験あり。",
                created_at=datetime.now() - timedelta(days=3),
            ),
        ]
        for memo in memos:
            db.add(memo)
        db.commit()
        print(f"✅ メモ作成: {len(memos)}件")
        
        # メール作成
        mails = [
            Mail(
                corner_id=corners[0].id,
                memo_id=memos[0].id,
                subject="街角スポットライト：駅前喫茶店の話",
                body="いつも番組を楽しく聴いています。\n\n駅前の喫茶店「珈琲の時間」のマスターに取材してきました...",
                status="下書き",
                created_at=datetime.now() - timedelta(hours=1),
                updated_at=datetime.now() - timedelta(hours=1),
            ),
            Mail(
                corner_id=corners[3].id,
                memo_id=None,
                subject="今日の一曲リクエスト",
                body="ラジオネーム太郎です。\n\n思い出の曲をリクエストさせてください...",
                status="送信済み",
                sent_at=datetime.now() - timedelta(days=5),
                created_at=datetime.now() - timedelta(days=5),
                updated_at=datetime.now() - timedelta(days=5),
            ),
            Mail(
                corner_id=corners[2].id,
                memo_id=None,
                subject="質問：コーヒーの淹れ方について",
                body="いつも楽しく聴いています。\n\n美味しいコーヒーの淹れ方を教えてください...",
                status="採用",
                sent_at=datetime.now() - timedelta(days=10),
                created_at=datetime.now() - timedelta(days=10),
                updated_at=datetime.now() - timedelta(days=8),
            ),
        ]
        for mail in mails:
            db.add(mail)
        db.commit()
        print(f"✅ メール作成: {len(mails)}件")
        
        print("\n✨ 初期データの投入が完了しました！")
        print(f"\n📊 投入データサマリー:")
        print(f"  - ユーザー: 1件")
        print(f"  - プロフィール: {len(profiles)}件")
        print(f"  - パーソナリティ: {len(personalities)}件")
        print(f"  - 番組: 3件")
        print(f"  - コーナー: {len(corners)}件")
        print(f"  - メモ: {len(memos)}件")
        print(f"  - メール: {len(mails)}件")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
