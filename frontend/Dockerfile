FROM python:3.11-slim

WORKDIR /app

# pipenvのインストール
RUN pip install --no-cache-dir pipenv

# 依存関係ファイルのコピーとインストール
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# アプリケーションコードのコピー
COPY . .

# ポート8501を公開
EXPOSE 8501

# Streamlitの起動
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]