# Dockerでのデプロイ

[100_memo_api](../100_memo_api/)（001〜025の集大成アプリ）をDockerコンテナとして動かす手順です。`python app.py`（Flaskの開発用サーバー）ではなく、本番向けのWSGIサーバー（`gunicorn`）で動かします。

## なぜDockerを使うのか

| 課題 | Dockerによる解決 |
|---|---|
| 「自分の環境では動くのに他の環境では動かない」 | OS・Pythonバージョン・依存パッケージをイメージに固定するため、どこで動かしても同じ結果になる |
| デプロイ先ごとに手順が違う（Render・Railway・AWSなど） | 多くのPaaS/クラウドが「Dockerfileを渡せばそのまま動かせる」仕組みを持っているため、1つのDockerfileが色々な環境で使い回せる |

## 用意したファイル

```
100_memo_api/app/
├── Dockerfile          イメージのビルド手順
├── entrypoint.sh        コンテナ起動時に実行されるスクリプト
├── docker-compose.yml   ビルド・起動をまとめて行うための設定
├── .dockerignore        イメージに含めないファイル（キャッシュ・DBファイルなど）
└── requirements.txt     このアプリが依存するパッケージ一覧
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

# マイグレーションはビルド時に1回だけ生成してイメージに焼き込む。
RUN flask db init && flask db migrate -m "initial migration"

RUN chmod +x entrypoint.sh

EXPOSE 5085

ENTRYPOINT ["./entrypoint.sh"]
```

| 命令 | 説明 |
|---|---|
| `FROM python:3.11-slim` | 土台となるイメージ（軽量版のPython 3.11） |
| `WORKDIR /app` | コンテナ内の作業ディレクトリ |
| `COPY requirements.txt .` → `RUN pip install` → `COPY . .` の順番 | 依存パッケージのインストールを先に済ませておくことで、アプリのコードだけを変更した際に`pip install`のレイヤーがキャッシュされ、再ビルドが速くなる |
| `RUN flask db init && flask db migrate` | マイグレーションファイルを**ビルド時に1回だけ**生成する（理由は次項） |
| `EXPOSE 5085` | コンテナがどのポートを使うかのドキュメント的な宣言（実際のポート公開は`docker run -p`や`docker-compose.yml`側で行う） |

**マイグレーションをビルド時に生成する理由**：もしコンテナ起動のたびに`flask db migrate`を実行すると、コンテナを作り直すたびに新しいリビジョンID（マイグレーションの識別子）が発行されます。DB側（永続化したvolume）にはすでに古いリビジョンIDが記録されているため、「そのリビジョンIDのマイグレーションが見つからない」というエラーで`flask db upgrade`が失敗します。ビルド時に1回だけ生成してイメージに焼き込み、起動時は`flask db upgrade`だけを実行することで、この食い違いを防いでいます。

### entrypoint.sh

```bash
#!/bin/sh
set -e

flask db upgrade

exec gunicorn --bind 0.0.0.0:5085 app:app
```

コンテナが起動するたびに、まず`flask db upgrade`でDBを最新のスキーマにしてから（初回はテーブルを作成、2回目以降は何もしない）、`gunicorn`でアプリを起動します。`python app.py`（Flaskの開発用サーバー）は同時に1つのリクエストしか処理できず、本番運用には向かないため、複数ワーカーで動く`gunicorn`に置き換えています。

### requirements.txt

```
Flask==2.3.3
Flask-WTF==1.2.2
Flask-Login==0.6.3
Flask-SQLAlchemy==3.0.3
Flask-Migrate==4.0.4
SQLAlchemy==2.0.48
requests==2.33.1
gunicorn==23.0.0
```

ルートの[README](../README.md#動作確認済みのライブラリバージョン)で動作確認済みとしているバージョンに、本番サーバー用の`gunicorn`を追加したものです。

### docker-compose.yml

```yaml
services:
  web:
    build: .
    ports:
      - "5085:5085"
    volumes:
      - instance_data:/app/instance
    environment:
      - SECRET_KEY=change-me-in-production

volumes:
  instance_data:
```

| 項目 | 説明 |
|---|---|
| `build: .` | このディレクトリの`Dockerfile`からイメージをビルドする |
| `ports` | ホストの5085番ポートをコンテナの5085番ポートに転送する |
| `volumes` | SQLiteのDBファイル（`instance/memos.sqlite`）をコンテナの外（Docker管理下の永続ボリューム）に保存し、コンテナを作り直してもデータが消えないようにする |
| `environment` | `SECRET_KEY`を環境変数で上書きする（後述） |

## 環境変数（SECRET_KEY）

`config.py`は`SECRET_KEY`を環境変数から読み込むようになっています。

```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
```

学習用に`python app.py`でローカル起動する場合は環境変数が無くても`'dev-secret-key'`が使われて動きますが、**本番で公開する場合は必ず環境変数で上書きしてください**。`SECRET_KEY`はセッションやCSRFトークンの署名に使われる値で、これが漏れる・推測されると、他人のセッションを偽造されるおそれがあります。

## 起動手順

### docker composeを使う場合（推奨）

```bash
cd 100_memo_api/app
docker compose up --build
```

`http://localhost:5085` にアクセスして動作を確認します。停止するときは`docker compose down`（`-v`を付けるとDBの永続化ボリュームごと削除されます）。

### docker composeを使わない場合

```bash
cd 100_memo_api/app
docker build -t memo-api .
docker run -p 5085:5085 -e SECRET_KEY=change-me-in-production -v memo_instance:/app/instance memo-api
```

## 動作確認

```bash
curl http://localhost:5085/auth/register
```

ブラウザで`http://localhost:5085/auth/register`から登録すると、最初に登録したユーザーが自動的に管理者になります（`024_role_management`で学んだ仕組み）。

## 本番のクラウド環境にデプロイする場合

RenderやRailwayなど「Dockerfileを渡すとそのままデプロイできる」PaaSであれば、このDockerfileをそのまま使えます。一般的な流れは以下の通りです。

1. GitHubにリポジトリをpushする（[GitHubにリポジトリをpushする手順](github.md)参照）
2. デプロイ先のサービスで「このリポジトリの`100_memo_api/app`ディレクトリをDockerfileからビルドする」ように設定する
3. `SECRET_KEY`を環境変数（Secrets）として設定する
4. デプロイ先が提供する永続ストレージ（ボリューム）を`/app/instance`にマウントする（設定しないとデプロイのたびにSQLiteのデータが消えます）

Renderでの具体的な手順は[Renderへのデプロイ手順](render.md)にまとめています。

**注意**：SQLiteは同時書き込みに弱く、小規模な学習用途向けのデータベースです。本格的な本番運用では、PostgreSQLなど別のデータベースサービスへの切り替えを検討してください（`SQLALCHEMY_DATABASE_URI`を環境変数から読み込むように`config.py`を変更する形になります）。

## トラブルシューティング

| 症状 | 原因・対処 |
|---|---|
| `docker: command not found` | Docker Desktop（またはDocker Engine）がインストールされていない。[公式サイト](https://www.docker.com/)からインストールする |
| `Cannot connect to the Docker daemon` | Docker Desktopが起動していない。アプリを起動してから再実行する |
| `flask db upgrade`で`Can't locate revision identified by '...'`エラー | イメージの再ビルド前後でマイグレーションの中身が変わったのに、古い永続化ボリュームが残っている場合に起こる。学習用途であれば`docker compose down -v`でボリュームごと削除してから作り直す |
| ポート`5085`がすでに使われている | 他のチャプターのFlaskアプリ（`ポート=5085`を使うもの）が起動したままになっていないか確認する。`docker-compose.yml`の`ports`の左側の数字（ホスト側）を空いている番号に変更してもよい |

## 次のステップ

Dockerでのローカル動作確認ができたら、[Renderへのデプロイ手順](render.md)でクラウドに公開してみましょう。
