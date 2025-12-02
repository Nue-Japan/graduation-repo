# 1. ベースイメージ (Python 3.12 Slim)
FROM python:3.12-slim

# 2. コンテナ内の作業ディレクトリ
WORKDIR /code

# 3. 依存ライブラリのインストール
# (キャッシュを有効活用するため、先にrequirements.txtだけコピーしてインストール)
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. ソースコードをコンテナにコピー
COPY . /code/

# 5. 起動コマンド
# (ホスト0.0.0.0で待ち受けないと、Dockerの外からアクセスできません)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]