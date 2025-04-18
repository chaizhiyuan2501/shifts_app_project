# Python 3.11 の公式イメージを使用
FROM python:3.11

# 環境変数を設定します（書き込みキャッシュ防止、バッファ抑制）
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 作業ディレクトリを設定
WORKDIR /app

# システム依存関係をインストールします（OpenCV / OCR 用含む）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Python の依存関係をインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# プロジェクトファイルをコピー
COPY . .

# ポート8000を公開
EXPOSE 8000