FROM pgvector/pgvector:pg16

# pgvectorのインストール
RUN apt-get update && \
    apt-get install -y \
    git \
    build-essential \
    postgresql-server-dev-16 && \
    rm -rf /var/lib/apt/lists/*

# 初期化スクリプトをコピー
COPY init.sql /docker-entrypoint-initdb.d/

ENV TZ Asia/Tokyo
ENV POSTGRES_DB=radio_corner_selector
ENV POSTGRES_USER=radio_user
ENV POSTGRES_PASSWORD=radio_password
