FROM python:3.11-slim

WORKDIR /app

# システムパッケージの更新とpipenvのインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir pipenv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 依存関係ファイルのコピーとインストール
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# アプリケーションコードのコピー
COPY . .

RUN chmod 755 entrypoint.sh

# ポート8000を公開
EXPOSE 8000

# Uvicornでアプリケーションを起動
CMD ["./entrypoint.sh"]
