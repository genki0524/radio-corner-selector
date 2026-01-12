FROM nvidia/cuda:12.5.1-devel-ubuntu22.04

RUN apt-get update && apt-get install -y python3.11 python3-pip && rm -rf /var/apt/lists/*

WORKDIR /app

COPY ./ /app

RUN pip install --no-cache-dir -r requirements.txt