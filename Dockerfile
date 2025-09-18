# Python イメージを利用
FROM python:3.13-slim

# 作業ディレクトリを設定
WORKDIR /app

# ライブラリをインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトをコピー
COPY . /app/

# ポート解放
EXPOSE 8000

# 起動コマンド
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
