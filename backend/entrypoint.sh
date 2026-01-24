#!/bin/bash

#データベースのマイグレーション
echo "Running Database Migrations..."
alembic upgrade head

#アプリケーションの起動
echo "Starting FastAPI Application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload