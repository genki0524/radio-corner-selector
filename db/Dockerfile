FROM postgres:16

# pgvectorのインストール
RUN apt-get update && \
    apt-get install -y \
    git \
    build-essential \
    postgresql-server-dev-16 && \
    rm -rf /var/lib/apt/lists/*

# pgvectorをビルドしてインストール
RUN git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git /tmp/pgvector && \
    cd /tmp/pgvector && \
    make && \
    make install && \
    rm -rf /tmp/pgvector

# 初期化スクリプトをコピー
COPY init.sql /docker-entrypoint-initdb.d/

ENV TZ Asia/Tokyo
# ENV LANG ja_JP.UTF-8
# ENV LANGUAGE ja_JP:ja
# ENV LC_ALL ja_JP.UTF-8
ENV POSTGRES_DB=radio_corner_selector
ENV POSTGRES_USER=radio_user
ENV POSTGRES_PASSWORD=radio_password
