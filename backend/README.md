# ラジオ投稿管理アプリ - バックエンドAPI

## 概要
FastAPIで構築されたRESTful API。ラジオ番組投稿管理のためのバックエンドサービスを提供します。

## 技術スタック
- **Framework:** FastAPI
- **Database:** SQLite (SQLAlchemy v2.0)
- **ORM:** SQLAlchemy
- **Schema Validation:** Pydantic v2
- **Settings Management:** Pydantic Settings
- **LLM:** Google Generative AI (Gemini)
- **Language:** Python 3.13
- **Web Server:** Uvicorn
- **Dependency Management:** Pipenv

## ディレクトリ構造
```
backend/
├── main.py                 # FastAPIアプリケーション
├── config.py              # 環境変数・設定
├── database.py            # データベース接続
├── models.py              # SQLAlchemyモデル
├── schemas.py             # Pydanticスキーマ
├── seed_data.py           # 初期データ投入スクリプト
├── Dockerfile             # Dockerコンテナ設定
├── Pipfile                # 依存関係
├── routers/               # APIルーター
│   ├── memos.py          # メモ管理
│   ├── profiles.py       # プロフィール管理
│   ├── personalities.py  # パーソナリティ管理
│   ├── programs.py       # 番組管理
│   ├── corners.py        # コーナー管理
│   ├── mails.py          # メール管理
│   └── analyze.py        # LLM解析
├── cruds/                 # データベース操作
│   ├── memos.py          # メモCRUD
│   ├── profiles.py       # プロフィールCRUD
│   ├── personalities.py  # パーソナリティCRUD
│   ├── programs.py       # 番組CRUD
│   ├── corners.py        # コーナーCRUD
│   ├── mails.py          # メールCRUD
│   └── analyze.py        # 解析関連CRUD
└── services/              # ビジネスロジック
    └── analyze_service.py # LLM解析サービス
```

## セットアップ

### 必要な環境
- Python 3.13以上
- Pipenv

### インストール
```bash
cd backend
# 環境変数を設定（必要に応じて）
# GEMINI_API_KEYを設定する場合は.envファイルを作成
pipenv install
```

### 環境変数の設定（オプション）
Google Gemini APIを使用する場合は、`.env`ファイルを作成して以下を設定：
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-pro
DATABASE_URL=sqlite:///./radio_corner_selector.db
CORS_ORIGINS=["http://localhost:8501","http://localhost:3000"]
```

※ APIキーが未設定の場合、モックレスポンスで動作します。

### データベース初期化
```bash
pipenv run python seed_data.py
```

### 起動方法
```bash
pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

APIは `http://localhost:8000` で起動します。

### API ドキュメント
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API エンドポイント

### メモ管理
- `GET /api/memos?user_id={user_id}` - メモ一覧取得
- `GET /api/memos/{memo_id}` - メモ詳細取得
- `POST /api/memos` - メモ作成
- `PUT /api/memos/{memo_id}` - メモ更新
- `DELETE /api/memos/{memo_id}` - メモ削除

### プロフィール管理
- `GET /api/profiles?user_id={user_id}` - プロフィール一覧取得
- `GET /api/profiles/{profile_id}` - プロフィール詳細取得
- `POST /api/profiles` - プロフィール作成
- `PUT /api/profiles/{profile_id}` - プロフィール更新
- `DELETE /api/profiles/{profile_id}` - プロフィール削除

### パーソナリティ管理
- `GET /api/personalities?user_id={user_id}` - パーソナリティ一覧取得
- `GET /api/personalities/{personality_id}` - パーソナリティ詳細取得
- `POST /api/personalities` - パーソナリティ作成
- `PUT /api/personalities/{personality_id}` - パーソナリティ更新
- `DELETE /api/personalities/{personality_id}` - パーソナリティ削除

### 番組管理
- `GET /api/programs?user_id={user_id}&personality_id={personality_id}&search={keyword}` - 番組一覧取得（絞り込み可能）
- `GET /api/programs/{program_id}` - 番組詳細取得
- `POST /api/programs` - 番組作成
- `PUT /api/programs/{program_id}` - 番組更新
- `DELETE /api/programs/{program_id}` - 番組削除

### コーナー管理
- `GET /api/corners?program_id={program_id}` - コーナー一覧取得
- `GET /api/corners/{corner_id}` - コーナー詳細取得
- `POST /api/corners` - コーナー作成
- `PUT /api/corners/{corner_id}` - コーナー更新
- `DELETE /api/corners/{corner_id}` - コーナー削除

### メール管理
- `GET /api/mails?user_id={user_id}&status_filter={status}` - メール一覧取得
- `GET /api/mails/stats?user_id={user_id}` - メール統計取得
- `GET /api/mails/{mail_id}` - メール詳細取得
- `POST /api/mails` - メール作成
- `PUT /api/mails/{mail_id}` - メール更新
- `DELETE /api/mails/{mail_id}` - メール削除

### LLM解析
- `POST /api/analyze` - メモを解析して最適なコーナーを推奨

## データベーススキーマ

ER図に基づいた以下のテーブル構成：

### テーブル一覧
- `users` - ユーザー（email, password_hash）
- `profiles` - プロフィール（投稿用署名：radio_name, real_name, address, phone）
- `personalities` - パーソナリティ（name, nickname）
- `programs` - 番組（title, email_address, broadcast_schedule, default_profile_id）
- `corners` - コーナー（title, description_for_llm）
- `memos` - メモ（content, created_at）
- `mails` - メール（subject, body, status, sent_at, created_at, updated_at）
- `program_personalities` - 番組とパーソナリティの多対多関係

### リレーション
- User → Profiles（1対多）
- User → Programs（1対多）
- User → Personalities（1対多）
- User → Memos（1対多）
- Program ↔ Personalities（多対多）
- Program → Corners（1対多）
- Program → default Profile（多対1）
- Corner → Mails（1対多）
- Memo → Mails（1対多、オプショナル）

詳細は [models.py](models.py) を参照してください。

## LLM機能

### Google Gemini API
メモの内容を解析し、最適なコーナーを推奨します。

#### 設定方法
1. Google AI Studioで APIキーを取得: https://makersuite.google.com/app/apikey
2. `.env`ファイルに`GEMINI_API_KEY`を設定

#### 解析ロジック
1. ユーザーのメモ内容と利用可能なすべてのコーナー情報を取得
2. Gemini APIに送信し、各コーナーの適合度を評価
3. 適合度スコア（0.0-1.0）と推奨理由をJSON形式で取得
4. スコアの高い順に最大3つのコーナーを返す

#### APIキーが未設定の場合
モックレスポンスを返すため、APIキーなしでも動作確認可能です。

#### 使用例
```bash
POST /api/analyze
{
  "user_id": 1,
  "memo_content": "最近ハマっている趣味について書きたい"
}
```

レスポンス：
```json
{
  "recommendations": [
    {
      "corner_id": 1,
      "program_title": "○○ラジオ",
      "corner_title": "趣味のコーナー",
      "score": 0.95,
      "reason": "趣味に関する投稿にぴったりのコーナーです"
    }
  ]
}
```

## 開発

### 開発サーバーの起動
```bash
pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker による起動
```bash
docker build -t radio-corner-selector-backend .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_api_key radio-corner-selector-backend
```

### テスト
```bash
pipenv run pytest
```

### コード整形（オプション）
```bash
pipenv install --dev black
pipenv run black .
```

### 型チェック（オプション）
```bash
pipenv install --dev mypy
pipenv run mypy .
```

## CORS設定

フロントエンドからのアクセスを許可するため、`config.py`でデフォルト設定されています：

```python
cors_origins: list[str] = ["http://localhost:8501", "http://localhost:3000"]
```

必要に応じて`.env`ファイルで上書き可能：
```
CORS_ORIGINS=["http://localhost:8501","http://localhost:3000","https://your-frontend.com"]
```

## トラブルシューティング

### データベースのリセット
```bash
rm radio_corner_selector.db
pipenv run python seed_data.py
```

### Gemini APIエラー
- APIキーが正しく設定されているか確認（`.env`ファイルまたは環境変数）
- [Google AI Studio](https://makersuite.google.com/)でAPIの利用制限に達していないか確認
- エラー時は自動的にモックレスポンスを返します

### CORS エラー
フロントエンドからのアクセスが拒否される場合、`config.py`または`.env`で適切なオリジンを設定：
```python
CORS_ORIGINS=["http://localhost:8501","http://localhost:3000"]
```

### データベース接続エラー
SQLiteファイルが作成されていない場合：
```bash
pipenv run python -c "from database import init_db; init_db()"
```

## ライセンス
MIT License

## アーキテクチャ

### レイヤー構造
```
┌─────────────────────────────────────┐
│   API Layer (routers/)              │
│   - HTTPリクエスト/レスポンス処理   │
│   - Pydanticスキーマによる検証      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Service Layer (services/)         │
│   - ビジネスロジック                │
│   - 外部API連携（Gemini）          │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   CRUD Layer (cruds/)               │
│   - データベース操作                │
│   - SQLAlchemyクエリ                │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Model Layer (models.py)           │
│   - データモデル定義                │
│   - リレーション定義                │
└─────────────────────────────────────┘
```

### 主要な機能フロー

#### メモ解析フロー
1. クライアント → `POST /api/analyze`
2. `routers/analyze.py` → リクエスト受信
3. `services/analyze_service.py` → Gemini APIで解析
4. `cruds/analyze.py` → ユーザーのコーナー情報取得
5. レスポンス返却（推奨コーナーリスト）

#### メール作成フロー
1. クライアント → `POST /api/mails`
2. `routers/mails.py` → リクエスト受信、検証
3. `cruds/mails.py` → データベースに保存
4. レスポンス返却（作成されたメール情報）
