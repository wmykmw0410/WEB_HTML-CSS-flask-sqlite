# Renderへのデプロイ手順

[Dockerでのデプロイ](docker.md)で作った`100_memo_api/app`のDockerfileを使って、[Render](https://render.com/)（無料枠のあるPaaS）に公開する手順です。GitHubにリポジトリをpushしてあることが前提です（未実施の場合は[GitHubにリポジトリをpushする手順](github.md)を参照してください）。

## 1. Web Serviceを作成する

1. Renderにサインアップ・ログインする
2. ダッシュボードで **New +** → **Web Service** を選ぶ
3. デプロイ対象のGitHubリポジトリを接続する
4. 設定画面で以下を入力する

| 項目 | 設定値 |
|---|---|
| Root Directory | `100_memo_api/app` |
| Runtime | **Docker**（Root Directoryに`Dockerfile`があると自動で選択される） |
| Instance Type | Free（学習用途であればこれで十分） |

Renderは`Dockerfile`の`EXPOSE`と`entrypoint.sh`の中身を見て、コンテナ内でアプリがどのポートで待ち受けているかを自動検出します。`docker-compose.yml`はローカル開発用のファイルなのでRenderは使いません。

## 2. 環境変数を設定する

**Environment** タブで以下を追加します。

| キー | 値 |
|---|---|
| `SECRET_KEY` | ランダムな文字列（Renderの「Generate」ボタンで自動生成できる） |

`config.py`が`os.environ.get('SECRET_KEY', 'dev-secret-key')`という書き方になっているため、これを設定するだけで本番用の値に切り替わります（[Dockerでのデプロイ](docker.md#環境変数secret_key)参照）。

## 3. デプロイする

設定を保存すると、RenderがGitHubのコードを取得してDockerイメージをビルドし、自動的にデプロイします。完了すると`https://<サービス名>.onrender.com`のようなURLが発行されます。

```bash
curl https://<サービス名>.onrender.com/auth/register
```

ブラウザで`/auth/register`にアクセスして、最初のユーザー登録（自動的に管理者になる）を確認してください。

以降、`main`ブランチにpushするたびに自動で再デプロイされます（Auto-Deployが既定で有効）。

## 4. データ永続化についての注意（重要）

**Renderの無料プランはファイルシステムがephemeral（一時的）です。** コンテナが再起動・再デプロイされるたびに、書き込んだファイル（`instance/memos.sqlite`）は失われます。ローカルのDockerでは`docker-compose.yml`の`volumes`で永続化していましたが、Render側で同じことをするには以下のいずれかが必要です。

| 方法 | 特徴 |
|---|---|
| Render Disks（永続ディスク） | `/app/instance`にディスクをマウントできるが、**有料プランのみ**の機能 |
| 外部のマネージドDBに切り替える | RenderのマネージドPostgreSQL（無料枠あり）などを使い、`config.py`の`SQLALCHEMY_DATABASE_URI`を環境変数から読み込むように変更する。学習用途を超えるが、実務ではこちらが一般的 |

無料プランのまま動作確認だけしたい場合は、「再デプロイするとデータが消える」ことを理解した上で使ってください。

## 5. 無料プランのスリープについて

Renderの無料プランのWeb Serviceは、一定時間アクセスが無いと自動的にスリープします。スリープ中に最初のアクセスが来ると、コンテナの起動に数十秒かかることがあります（すぐに開かなくてもエラーではありません）。

## トラブルシューティング

| 症状 | 原因・対処 |
|---|---|
| ビルドは成功するがアクセスすると502エラー | `entrypoint.sh`内の`gunicorn --bind 0.0.0.0:5085`のポート番号と、Renderが検出したポートが一致していない可能性がある。`Dockerfile`の`EXPOSE`の値と`entrypoint.sh`の`--bind`の値が同じになっているか確認する |
| デプロイ後に登録したはずのユーザーが消えている | [データ永続化についての注意](#4-データ永続化についての注意重要)を参照。無料プランはephemeralなファイルシステムのため想定通りの挙動 |
| `SECRET_KEY`を設定したのに反映されない | 環境変数を追加・変更した後は手動で再デプロイ（Manual Deploy）が必要な場合がある |

## 次のステップ

学習用のデプロイ体験としてはここまでで十分です。実務でPostgreSQLなどの永続DBに切り替える場合は、[Dockerでのデプロイ](docker.md#本番のクラウド環境にデプロイする場合)の注意点も参照してください。
