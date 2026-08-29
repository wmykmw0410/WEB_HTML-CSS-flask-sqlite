# 郵便番号・写真の登録機能を追加

日付: 2026-08-29

## これは何をする作業か

登録フォームに「郵便番号」と「写真」の入力欄を追加し、DBにも保存できるようにする。

## 手順

1. `trash_map/form.py` に2つのフィールドを追加する。
   - `postal_code`（`StringField`） — 入力は任意（`validators.Optional()`）だが、もし入力された場合は `123-4567` の形式かどうかを正規表現（`validators.Regexp(r"^\d{3}-?\d{4}$", ...)`）でチェックする。
   - `photo`（`flask_wtf.file.FileField`） — 任意項目。`FileAllowed(["jpg", "jpeg", "png", "gif"], ...)` で、指定した拡張子以外のファイルはアップロードできないようにする。
2. `trash_map/models.py` にカラムを追加する。
   ```python
   postal_code = db.Column(db.String(10), nullable=True)
   photo_filename = db.Column(db.String(255), nullable=True)
   ```
   - 写真そのもの（バイナリデータ）をDBに入れるのではなく、`static/uploads/` に保存したあとの**ファイル名だけ**をDBに持たせる設計にしている。
3. モデルにカラムを追加しても、`db.create_all()` は既存のテーブルを自動では更新してくれない。そのため、SQLiteに対して直接コマンドを実行してカラムを追加する。
   ```sql
   ALTER TABLE trash_cans ADD COLUMN postal_code VARCHAR(10);
   ALTER TABLE trash_cans ADD COLUMN photo_filename VARCHAR(255);
   ```
   （当時テーブルにはまだデータが無かったため、データが消える心配はなかった。以後モデルにカラムを追加するたびに、同様の手動作業が必要になる点に注意）
4. `trash_map/app.py` に写真のアップロード処理を追加する。
   - `basedir/static/uploads/` フォルダを保存先として作成し、`app.config['UPLOAD_FOLDER']` に設定する。
   - `app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024` で、アップロードできるファイルサイズの上限を5MBに制限する。
   - `add_page` 関数の中で、`secure_filename()` を使ってアップロードされた元のファイル名を安全な形に変換し、拡張子だけを取り出す。さらに `uuid.uuid4().hex` でランダムなファイル名を生成し、拡張子とつなげて保存する（同じ名前のファイルが上書きされてしまう事故や、悪意あるファイル名によるパストラバーサル攻撃を防ぐため）。DBにはこの生成後のファイル名だけを保存する。
5. テンプレートを更新する。
   - `trash_map/templates/trash/add.html` の `<form>` タグに `enctype="multipart/form-data"` を追加する（これがないとファイルがサーバーに送信されない）。郵便番号・写真の入力欄も追加する。
   - `trash_map/templates/trash/type_list.html` のテーブルに「郵便番号」「写真」の列を追加する。写真は `item.photo_filename` が設定されていれば `<img>` タグでサムネイル表示する。

## 動作確認

1. 郵便番号「100-0005」とjpg画像を指定して登録し、`302 /thankyou` になること、DBに `postal_code` と `photo_filename` が正しく保存されることを確認する。
2. 郵便番号に不正な形式（例: `abcde`）を入力して送信し、`200`（バリデーションエラー「郵便番号の形式が正しくありません」が表示される）になることを確認する。
3. 許可していない拡張子のファイル（例: `malware.exe`）をアップロードしようとして、`200`（バリデーションエラー「画像ファイル（jpg, jpeg, png, gif）のみアップロードできます」が表示される）になることを確認する。
4. `/list/can` などで、登録した郵便番号とサムネイル画像が一覧に表示されることを確認する。
5. 確認が終わったら、テスト用に登録したDBレコードとアップロードした画像ファイルは削除しておく。
