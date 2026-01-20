# コーナー推薦システム - 使用ガイド

## 概要

このシステムは、**ベクトル検索**と**LLM推論**を組み合わせて、メモ内容から最適なラジオコーナーを推薦します。

### 使用技術

- **LangChain**: LLMアプリケーション開発フレームワーク
- **HuggingFace Embeddings**: テキスト埋め込み生成
  - モデル: `intfloat/multilingual-e5-large` (1024次元)
- **Ollama**: ローカルLLM推論
  - モデル: `Qwen 2.5`
- **pgvector**: PostgreSQLベクトル類似度検索

## セットアップ

### 1. 依存関係のインストール

```bash
pipenv install langchain langchain-ollama langchain-huggingface langchain-postgres
```

### 2. Ollamaのインストールと起動

```bash
# Ollamaをインストール（macOS）
brew install ollama

# Ollamaサービスを起動
ollama serve

# Qwen 2.5モデルをダウンロード
ollama pull qwen2.5:latest
```

### 3. 環境変数の設定

`.env`ファイルに以下を追加:

```env
# LangChain & LLM Settings
EMBEDDING_MODEL_NAME=intfloat/multilingual-e5-large
EMBEDDING_DIMENSION=1024
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:latest
OLLAMA_TEMPERATURE=0.7
```

### 4. データベースマイグレーション

`embedded_description`カラムが1024次元に更新されているか確認してください。

```sql
-- 既存のデータベースの場合、カラムを変更
ALTER TABLE corners 
ALTER COLUMN embedded_description TYPE vector(1024);
```

## 使用方法

### 1. 埋め込みベクトルの生成

新しいコーナーを作成したり、既存のコーナーを更新した後、埋め込みベクトルを生成する必要があります。

#### 特定のコーナーの埋め込みを更新

```bash
curl -X POST "http://localhost:8000/api/recommendations/embeddings/update" \
  -H "Content-Type: application/json" \
  -d '{
    "corner_id": 1
  }'
```

#### 特定ユーザーの全コーナーを一括更新

```bash
curl -X POST "http://localhost:8000/api/recommendations/embeddings/update" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1
  }'
```

#### 全コーナーを一括更新

```bash
curl -X POST "http://localhost:8000/api/recommendations/embeddings/update" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 2. コーナー推薦

#### 複数のコーナーを推薦（詳細版）

```bash
curl -X POST "http://localhost:8000/api/recommendations/corners" \
  -H "Content-Type: application/json" \
  -d '{
    "memo_content": "最近、職場で面白いことがあったんです。同僚が...",
    "user_id": 1,
    "top_k": 10,
    "use_llm": true,
    "final_results": 3
  }'
```

**レスポンス例:**

```json
{
  "recommendations": [
    {
      "id": 1,
      "title": "職場あるある",
      "description_for_llm": "職場でのユニークな体験談を募集",
      "program_id": 1,
      "similarity": 0.85,
      "llm_score": 0.92,
      "score": 0.89,
      "confidence": "高信頼度",
      "reasoning": "職場での体験談という内容がコーナーのテーマと完全に一致しています。"
    },
    {
      "id": 2,
      "title": "日常の発見",
      "description_for_llm": "日常生活での小さな発見や気づき",
      "program_id": 1,
      "similarity": 0.72,
      "llm_score": 0.65,
      "score": 0.68,
      "confidence": "中信頼度",
      "reasoning": "職場も日常の一部ですが、専門的な体験談向けのコーナーがより適切です。"
    }
  ],
  "metadata": {
    "memo_content": "最近、職場で面白いことがあったんです...",
    "method": "vector_search_with_llm",
    "candidates_found": 10,
    "top_results": 2
  }
}
```

#### 最適なコーナーを1つだけ推薦（シンプル版）

```bash
curl -X POST "http://localhost:8000/api/recommendations/corners/single?memo_content=今日、猫が変な行動をしていました&user_id=1"
```

### 3. ヘルスチェック

推薦システムが正常に動作しているか確認:

```bash
curl http://localhost:8000/api/recommendations/health
```

**レスポンス例:**

```json
{
  "status": "healthy",
  "embedding_service": "ok",
  "embedding_dimension": 1024,
  "llm_service": "ok"
}
```

## アーキテクチャ

### 推薦フロー

1. **埋め込み生成**: メモ内容を`intfloat/multilingual-e5-large`で1024次元ベクトルに変換
2. **ベクトル検索**: pgvectorを使用してコサイン類似度で候補コーナーを検索（top_k件）
3. **LLM評価**: Qwen 2.5を使用して各候補の適合度を評価
4. **スコア統合**: ベクトル類似度(40%)とLLMスコア(60%)を加重平均
5. **ランキング**: 統合スコアでソートして上位を返却

### スコアリング方式

- **similarity_score**: ベクトル類似度 (0.0-1.0)
- **llm_score**: LLMによる評価 (0.0-1.0)
- **score**: 統合スコア = `similarity * 0.4 + llm_score * 0.6`
- **confidence**: 信頼度レベル
  - 高信頼度: score >= 0.8
  - 中信頼度: 0.3 <= score < 0.8
  - 低信頼度: score < 0.3

## パラメータ調整

### config.pyでの調整

```python
# 埋め込みモデルの変更
embedding_model_name: str = "intfloat/multilingual-e5-large"

# Ollamaの設定
ollama_model: str = "qwen2.5:latest"
ollama_temperature: float = 0.7  # 0.0-1.0、高いほど創造的

# 埋め込みベクトルの次元
embedding_dimension: int = 1024
```

### APIリクエストでの調整

```python
{
  "top_k": 10,          # ベクトル検索の候補数 (1-50)
  "use_llm": true,      # LLM推論を使用するか
  "final_results": 3    # 最終的に返却する推薦数 (1-10)
}
```

## トラブルシューティング

### Ollamaに接続できない

```bash
# Ollamaが起動しているか確認
ps aux | grep ollama

# 再起動
ollama serve
```

### 埋め込み生成が遅い

初回実行時は、HuggingFaceからモデルをダウンロードするため時間がかかります。
モデルは`~/.cache/huggingface/`にキャッシュされます。

### ベクトル次元エラー

`embedded_description`カラムの次元が1024になっているか確認してください。

```sql
SELECT attname, atttypmod 
FROM pg_attribute 
WHERE attrelid = 'corners'::regclass 
AND attname = 'embedded_description';
```

## APIドキュメント

起動後、以下のURLでSwagger UIを確認できます:
- http://localhost:8000/docs

## パフォーマンス最適化

### 埋め込み生成の最適化

- GPUがある場合: `model_kwargs={'device': 'cuda'}`に変更
- バッチ処理: `bulk_update_embeddings()`を使用

### ベクトル検索の最適化

```sql
-- インデックス作成（IVFFlat）
CREATE INDEX ON corners USING ivfflat (embedded_description vector_cosine_ops)
WITH (lists = 100);

-- または HNSW（より高速だがメモリ使用量大）
CREATE INDEX ON corners USING hnsw (embedded_description vector_cosine_ops);
```

## 今後の拡張

- [ ] RAG（Retrieval-Augmented Generation）による詳細な推薦理由生成
- [ ] ユーザーフィードバックによる推薦精度の向上
- [ ] 複数メモの一括推薦API
- [ ] リアルタイム埋め込み生成（コーナー作成時に自動生成）
