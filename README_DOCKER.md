# Docker環境での起動方法

## 前提条件
- Docker Desktop がインストールされていること
- Docker Compose が使用可能であること

## セットアップ手順

### 1. 環境変数の設定
プロジェクトルートに `.env` ファイルを作成し、Google Gemini APIキーを設定してください。

```bash
cp .env.example .env
```

`.env` ファイルを編集:
```
GEMINI_API_KEY=あなたのAPIキー
```

### 2. Dockerコンテナの起動

```bash
# コンテナのビルドと起動
docker-compose up -d

# ログの確認
docker-compose logs -f
```

### 3. アクセス
- **Frontend (Streamlit)**: http://localhost:8501
- **Backend (FastAPI)**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs

### 4. コンテナの停止

```bash
# コンテナの停止
docker-compose down

# コンテナ、ボリューム、イメージをすべて削除
docker-compose down -v --rmi all
```

## 便利なコマンド

```bash
# コンテナの再ビルド
docker-compose build

# 特定のサービスのみ起動
docker-compose up backend

# コンテナ内でコマンド実行
docker-compose exec backend bash
docker-compose exec frontend bash

# ログの確認（特定のサービス）
docker-compose logs -f backend
docker-compose logs -f frontend
```

## トラブルシューティング

### ポートが既に使用されている場合
`docker-compose.yaml` のポート設定を変更してください:
```yaml
ports:
  - "8001:8000"  # backend
  - "8502:8501"  # frontend
```

### データベースの初期化
```bash
docker-compose exec backend python seed_data.py
```
