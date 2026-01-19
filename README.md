# ラジオ投稿管理アプリ - 統合ガイド

## 🎉 完成したシステム

フロントエンドとバックエンドの統合が完了しました！

### アーキテクチャ

```
┌─────────────────────────────────────────────┐
│         Streamlit Frontend (8501)           │
│  - ダッシュボード                            │
│  - メモ管理                                  │
│  - 番組管理                                  │
│  - メール作成                                │
│  - プロフィール設定                          │
└───────────────┬─────────────────────────────┘
                │ HTTP REST API
                │ requests
                ↓
┌─────────────────────────────────────────────┐
│         FastAPI Backend (8000)              │
│  - RESTful API                              │
│  - SQLAlchemy ORM                           │
│  - Google Gemini API                        │
│  - SQLite Database                          │
└─────────────────────────────────────────────┘
```

## 🚀 起動方法

### 1. バックエンドAPIの起動

```bash
# ターミナル1
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

APIは `http://localhost:8000` で起動します。

- **API ドキュメント:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 2. フロントエンドの起動

```bash
# ターミナル2
cd frontend
streamlit run app.py
```

アプリは `http://localhost:8501` で起動します。

## 📊 機能一覧

### ✅ 実装済み機能

#### 1. メモ管理
- ✅ メモ一覧表示（API連携）
- ✅ メモ作成（API連携）
- ✅ メモ削除（API連携）
- ✅ メモ検索（クライアント側フィルタリング）

#### 2. 番組管理
- ✅ 番組一覧表示（API連携）
- ✅ 番組作成（コーナーと同時作成、API連携）
- ✅ 番組削除（API連携）
- ✅ パーソナリティでの絞り込み（API連携）
- ✅ 番組名での部分一致検索（API連携）
- ✅ コーナー一覧表示（API連携）

#### 3. メール作成
- ✅ メモ選択（API連携）
- ✅ AI解析による推奨コーナー（Gemini API連携）
- ✅ 手動コーナー選択（API連携）
- ✅ プロフィール選択（API連携）
- ✅ メール下書き保存（API連携）
- ✅ OS標準メーラー起動（mailto連携）

#### 4. プロフィール設定
- ✅ プロフィール一覧表示（API連携）
- ✅ プロフィール作成（API連携）
- ✅ プロフィール削除（API連携）
- ✅ メール署名プレビュー

#### 5. ダッシュボード
- ✅ クイックメモ入力（API連携）
- ✅ 投稿統計表示（API連携）
- ✅ 最近のメモ表示（API連携）

## 🔧 API エンドポイント

### メモ管理
```
GET    /api/memos?user_id={id}           # メモ一覧
POST   /api/memos                         # メモ作成
DELETE /api/memos/{memo_id}               # メモ削除
```

### 番組管理
```
GET    /api/programs?user_id={id}        # 番組一覧
       &personality_id={id}               # パーソナリティ絞り込み
       &search={keyword}                  # 番組名検索
POST   /api/programs                      # 番組作成
DELETE /api/programs/{program_id}        # 番組削除
```

### プロフィール管理
```
GET    /api/profiles?user_id={id}        # プロフィール一覧
POST   /api/profiles                      # プロフィール作成
DELETE /api/profiles/{profile_id}        # プロフィール削除
```

### メール管理
```
GET    /api/mails?user_id={id}           # メール一覧
GET    /api/mails/stats?user_id={id}     # メール統計
POST   /api/mails                         # メール作成
```

### LLM解析
```
POST   /api/analyze                       # メモ解析・コーナー推奨
```

## 🤖 AI機能（Google Gemini）

### 設定方法

1. Google AI Studioで APIキーを取得
   - https://makersuite.google.com/app/apikey

2. バックエンドの `.env` ファイルに設定
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

### 動作

- メモの内容とすべてのコーナー説明を解析
- 適合度スコア（0.0-1.0）付きで最大3つのコーナーを推奨
- APIキー未設定時はモックレスポンスを返す

## 📝 使用例

### 1. メモを作成

1. ダッシュボードの「クイックメモ」に内容を入力
2. 「追加」ボタンをクリック
3. メモがデータベースに保存される

### 2. 番組を作成

1. 「番組管理」ページを開く
2. 「新規番組を登録」を展開
3. 番組情報とコーナーを入力
4. 「登録」ボタンをクリック

### 3. AIでコーナーを推奨

1. 「メール作成」ページを開く
2. メモを選択
3. AIが自動で最適なコーナーを推奨
4. 「このコーナーに投稿」をクリック

### 4. メールを送信

1. 件名と本文を編集
2. 「メーラーで開く」をクリック
3. OS標準メーラーが起動
4. メール送信

## 🗄️ データベース

### 初期データ

seed_data.pyで以下のデータが投入されます：

- ユーザー: 1件
- プロフィール: 2件
- パーソナリティ: 4件
- 番組: 3件
- コーナー: 7件
- メモ: 5件
- メール: 3件

### データベースリセット

```bash
cd backend
rm radio_corner_selector.db
python seed_data.py
```

## 🐛 トラブルシューティング

### バックエンドに接続できない

```bash
# バックエンドが起動しているか確認
curl http://localhost:8000/

# 起動していない場合
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### フロントエンドでエラーが表示される

1. バックエンドが起動しているか確認
2. ブラウザのコンソールでエラーを確認
3. Streamlitを再起動

```bash
# Streamlit再起動
cd frontend
streamlit run app.py
```

### Gemini APIエラー

- APIキーが正しく設定されているか確認
- APIの利用制限に達していないか確認
- エラー時は自動的にモックレスポンスを返す

## 📚 技術スタック

### フロントエンド
- **Framework:** Streamlit
- **HTTP Client:** requests
- **Language:** Python

### バックエンド
- **Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy v2.0
- **Schema:** Pydantic v2
- **LLM:** Google Generative AI (Gemini)
- **Language:** Python

## 🎯 次のステップ

### 今後の拡張予定

1. **認証機能**
   - ユーザー登録・ログイン
   - JWTトークン認証

2. **編集機能**
   - 番組編集
   - プロフィール編集
   - メモ編集

3. **高度な機能**
   - メール送信履歴
   - 採用率の統計
   - エクスポート機能

4. **UI/UX改善**
   - ダークモード
   - レスポンシブデザイン
   - 通知機能

## 📄 ライセンス

（プロジェクトのライセンスを記載）

## 👥 貢献

（コントリビューションガイドを記載）
