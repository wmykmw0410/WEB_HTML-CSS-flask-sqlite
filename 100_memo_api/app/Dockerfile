FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

# マイグレーションはビルド時に1回だけ生成してイメージに焼き込む。
# コンテナ起動のたびに生成すると、再作成のたびにリビジョンIDが変わり、
# 永続化したDB（volumeのalembic_versionテーブル）と食い違ってしまうため。
RUN flask db init && flask db migrate -m "initial migration"

RUN chmod +x entrypoint.sh

EXPOSE 5085

ENTRYPOINT ["./entrypoint.sh"]
