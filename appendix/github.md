# GitHubにリポジトリをpushする手順（Git・GitHub初学者向け）

[Renderへのデプロイ手順](render.md)などクラウドサービスへのデプロイは、多くの場合「GitHubのリポジトリと連携する」形で行います。ここでは、Git・GitHubを初めて使う人向けに、基本の考え方からローカルのプロジェクトをGitHubにpushするまでを説明します。

## 1. GitとGitHubの違い

名前が似ていますが、役割が違う別々のものです。

| | 役割 |
|---|---|
| **Git** | ファイルの変更履歴を記録・管理する**ツール**（自分のパソコンの中だけで完結する） |
| **GitHub** | Gitのリポジトリ（後述）をインターネット上に保管し、他の人と共有できるようにする**サービス**（Webサイト） |

例えるなら、Gitは「変更履歴を保存できる高機能なフォルダ」、GitHubは「そのフォルダをアップロードしておける倉庫」です。Gitだけでも自分のパソコン内でバージョン管理はできますが、他の人と共有したり、別の場所（クラウドサービスなど）から参照したりするためにGitHubを使います。

## 2. 基本用語

| 用語 | 意味 |
|---|---|
| リポジトリ（repository） | 変更履歴ごと管理されているプロジェクトのフォルダ |
| コミット（commit） | 「この時点の変更内容」を記録するスナップショット。こまめに作る |
| ステージング（staging） | 「次のコミットに含めるファイル」を選んでおく場所 |
| リモート（remote） | 手元のリポジトリと紐づけた、GitHub上などにあるリポジトリの参照先 |
| ブランチ（branch） | 作業の分岐。特に指示がなければ`main`という名前のブランチを使う |
| push | 手元のコミットをリモート（GitHubなど）に送ること |
| pull / clone | リモートの内容を手元に持ってくること（`clone`は新規に丸ごとコピー、`pull`は既存リポジトリへの反映） |

## 3. Gitの初期設定（パソコンごとに最初の1回だけ）

まずGitがインストールされているか確認します。

```bash
git --version
```

バージョンが表示されればインストール済みです。表示されない場合は[公式サイト](https://git-scm.com/)からインストールしてください。

次に、コミットに記録される名前とメールアドレスを設定します（これはコミットの「作者情報」として記録されるもので、GitHubへのログイン情報とは別物です）。

```bash
git config --global user.name "あなたの名前"
git config --global user.email "your-email@example.com"
```

`--global`を付けると、このパソコン上のすべてのリポジトリで共通の設定になります。一度設定すれば、以降のプロジェクトで毎回設定し直す必要はありません。

## 4. ローカルでの基本的な流れ

GitHubに触れる前に、Git単体での基本の流れを押さえます。ファイルの状態は次の3段階で管理されています。

```
作業ディレクトリ  --git add-->  ステージング  --git commit-->  リポジトリ（コミット履歴）
（普段編集する場所）           （次のコミットの準備）          （確定した変更履歴）
```

| コマンド | 説明 |
|---|---|
| `git init` | 今いるフォルダをGitで管理し始める（最初の1回だけ） |
| `git status` | 今どのファイルが変更されている・ステージングされているかを確認する（迷ったらまずこれ） |
| `git add <ファイル名>` / `git add .` | 変更したファイルをステージングに追加する（`.`はカレントディレクトリ以下すべて） |
| `git commit -m "変更内容"` | ステージングした内容を1つの記録（コミット）として確定する |
| `git log` | これまでのコミット履歴を確認する |

```bash
cd プロジェクトのフォルダ
git init                        # このフォルダをGit管理下にする（最初の1回だけ）
git status                      # 状態を確認（すべて「Untracked files」と表示されるはず）
git add .                       # すべての変更をステージングに追加
git commit -m "Initial commit"  # 最初のコミットを作成
```

`git commit -m "..."` の`"..."`の部分は**コミットメッセージ**と呼ばれ、「何を変更したか」を短くまとめた説明文です。後で履歴を見返すときの手がかりになるので、`"fix"`のような曖昧な文言ではなく、内容が分かるように書く習慣をつけましょう。

## 5. コミットしてはいけないファイルを除外する（.gitignore）

DBファイルやキャッシュなど、環境ごとに生成される・人によって内容が変わるファイルはコミットしません。リポジトリ直下に`.gitignore`というファイルを作り、除外したいパターンを書きます。

```
__pycache__/
*.pyc
*.pyo
*.db
*.sqlite
*.sqlite3
instance/
migrations/
.pytest_cache/
.env
```

| パターン | 除外する理由 |
|---|---|
| `__pycache__/` / `*.pyc` / `*.pyo` | Pythonが自動生成するキャッシュファイル。実行するたびに再生成されるためコミット不要 |
| `*.db` / `*.sqlite` / `*.sqlite3` / `instance/` | SQLiteのDBファイル。各自の手元データであり、他人の環境に持ち込むべきではない |
| `migrations/` | `flask db init`で生成されるマイグレーション管理フォルダ。本カリキュラムの各チャプターでは各自が手元で生成する前提のため、リポジトリには含めない（[Dockerでのデプロイ](docker.md)ではDockerイメージのビルド時に生成し直している） |
| `.env` | `SECRET_KEY`など、秘密情報を書く可能性のあるファイル |

`.gitignore`に書いたファイルは`git status`にも`git add .`にも出てこなくなります。

**注意**：すでにコミットしてしまったファイルは、後から`.gitignore`に追加しても追跡が止まりません。誤ってコミットしていた場合は次のコマンドで追跡から外します（ファイル自体は手元に残ります）。

```bash
git rm -r --cached instance migrations
```

## 6. GitHubでアカウントを作り、空のリポジトリを作成する

1. [GitHub](https://github.com/)にアクセスし、アカウントを作成（すでにお持ちならログイン）する
2. 右上の **+** → **New repository** を選ぶ
3. リポジトリ名を入力する（例: `my-flask-app`）
4. **Public**（誰でも見られる）か**Private**（自分だけ）かを選ぶ。学習用なら公開してよければPublicで問題ありません
5. **README・.gitignore・LICENSEは追加しない**（チェックを入れない）。すでに手元にあるプロジェクトをpushする場合、GitHub側で先にこれらを作ってしまうと、手元の履歴とぶつかる原因になります
6. **Create repository** をクリックする

作成が終わると、`https://github.com/<ユーザー名>/<リポジトリ名>.git` のようなURLが発行された画面が表示されます。このURLは次の手順で使うので控えておきます。

## 7. ローカルのリポジトリとGitHubを繋いでpushする

「4. ローカルでの基本的な流れ」まで終わっている（`git init`してコミット済み）前提で進めます。

```bash
git remote add origin https://github.com/<ユーザー名>/<リポジトリ名>.git
git branch -M main
git push -u origin main
```

| コマンド | 説明 |
|---|---|
| `git remote add origin <URL>` | 手元のリポジトリに「origin」という名前でGitHub上のリポジトリを紐づける（`origin`は慣習的に使われる名前） |
| `git branch -M main` | 現在のブランチ名を`main`に変更する（デフォルトブランチ名を統一する） |
| `git push -u origin main` | `main`ブランチをGitHubにpushする。`-u`を付けると、以降は`git push`だけでこの紐づけ先にpushできるようになる |

```
[作業ディレクトリ] -- add --> [ステージング] -- commit --> [手元のリポジトリ]
                                                                    |
                                                                  push
                                                                    ↓
                                                        [GitHub上のリポジトリ (origin)]
```

pushが終わったら、GitHub上のリポジトリページを再読み込みしてファイル一覧が反映されているか確認してください。

### すでにリモートが設定されているか確認する

このリポジトリのように、すでに誰か（または過去の自分）が`git remote add`を済ませている場合もあります。

```bash
git remote -v
```

`origin`が表示されればすでに連携済みです。その場合は`git remote add`をやり直す必要はなく、2回目以降と同じ手順で進められます。

## 8. 2回目以降：変更を反映する

最初のpushが終わったら、以降はファイルを変更するたびに次の3つを繰り返すだけです。

```bash
git status                    # 何が変更されたか確認（習慣にすると安心）
git add .
git commit -m "変更内容の説明"
git push
```

## トラブルシューティング

| 症状 | 原因・対処 |
|---|---|
| `git: command not found` | Gitがインストールされていない。[公式サイト](https://git-scm.com/)からインストールする |
| `fatal: not a git repository` | `git init`していないフォルダでコマンドを実行している。プロジェクトのフォルダに移動してから`git init`する |
| `fatal: remote origin already exists` | すでに`origin`という名前でリモートが設定されている。`git remote -v`で確認し、URLを変更したい場合は`git remote set-url origin <新しいURL>`を使う |
| `Updates were rejected because the remote contains work that you do not have locally` | GitHub側にローカルに無いコミット（README生成など）がある。`git pull origin main --allow-unrelated-histories`で取り込んでからpushし直す |
| pushしたのに`instance/`や`*.sqlite`がGitHub上に見える | `.gitignore`を追加する前にコミットしてしまっている。「5. コミットしてはいけないファイルを除外する」の`git rm -r --cached`で追跡を外してから再度コミット・pushする |
| GitHubへのpushでユーザー名・パスワードを求められて失敗する | GitHubはパスワード認証を廃止済み。[Personal Access Token](https://docs.github.com/ja/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)を発行してパスワード欄に使うか、SSH鍵での認証に切り替える |

## 次のステップ

GitHubへのpushができたら、[Renderへのデプロイ手順](render.md)に進んでください。
