# 更新日と編集ページを追加

日付: 2026-08-29

## これは何をする作業か

登録したゴミ箱データを後から修正できる「編集ページ」を追加し、あわせて「いつ最後に更新されたか」を記録する `updated_at` カラムをDBに追加する。

## 手順

### 1. 更新日時カラムを追加する

1. `trash_map/models.py` に、現在時刻（UTC）を返す小さな関数と、更新日時のカラムを追加する。
   ```python
   def _utcnow():
       return datetime.now(timezone.utc)

   updated_at = db.Column(db.DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)
   ```
   `onupdate=_utcnow` を指定しておくと、そのレコードのどれか1つでもカラムが変更されてコミットされるたびに、SQLAlchemyが自動的に現在時刻を設定してくれる。ビュー関数の中で「更新日時をセットする」処理を自分で書く必要がない。
2. 既存のテーブルに新しいカラムを追加する。まず `nullable`（空でもOK）な状態でカラムだけ追加し、既存の行にはあとから現在時刻を入れる（バックフィル）。
   ```sql
   ALTER TABLE trash_cans ADD COLUMN updated_at DATETIME;
   UPDATE trash_cans SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL;
   ```
   最初は `NOT NULL DEFAULT CURRENT_TIMESTAMP` を一度に指定しようとしたが、使っているSQLiteのバージョンでは `Cannot add a column with non-constant default` というエラーになったため、上記の2段階に分けて対応した。

### 2. フォームの入力欄を使い回せるようにする

3. `trash_map/templates/trash/_garbage_form_fields.html` を新規作成し、`add.html` にあったフォームの入力欄（名前・住所・郵便番号・緯度経度・ゴミの種類チェックボックス・写真）をそのまま移す。これを `{% include "trash/_garbage_form_fields.html" %}` と書くだけで、登録用フォームと編集用フォームの両方から同じ入力欄を使い回せるようになる（同じHTMLを2箇所に書かずに済む）。

### 3. 編集ルートを追加する

4. `trash_map/app.py` に編集ページのルートを追加する。
   ```python
   @app.route("/trash/<int:trash_id>/edit", methods=['GET', 'POST'])
   def edit_page(trash_id):
       trash_can = db.get_or_404(TrashCan, trash_id)
       form = AddGarbageForm(
           name=trash_can.name, address=trash_can.address, postal_code=trash_can.postal_code,
           latitude=trash_can.latitude, longitude=trash_can.longitude,
           type=trash_can.type.split(",")
       )
       if form.validate_on_submit():
           # 各フィールドをtrash_canに反映。写真は新規アップロードがあった場合のみ差し替え
           db.session.commit()
           return redirect(url_for("detail_page", trash_id=trash_can.id))
       return render_template("trash/edit.html", form=form, item=trash_can)
   ```
   **なぜ `AddGarbageForm(obj=trash_can)` という書き方にしなかったのか:**
   DB上の `TrashCan.type` はカンマ区切りの生の文字列（例: `"burnable,can"`）で保存されている。もし `obj=trash_can` の形でフォームを初期化すると、複数選択用の `SelectMultipleField` がこの文字列を1文字ずつ（`"b"`, `"u"`, `"r"`, ...）反復してしまい、チェックボックスの初期選択が正しく表示されない不具合が起きる。これを避けるため、`type=trash_can.type.split(",")` のように事前にリストへ変換してから、他のフィールドと一緒に個別のキーワード引数として渡している。
   - 写真は必須にしていない。新しいファイルがアップロードされたときだけ `photo_filename` を差し替え、アップロードがなければ元の写真をそのまま残す。

### 4. 編集用テンプレートを作る

5. `trash_map/templates/trash/edit.html` を新規作成する。`_garbage_form_fields.html` を使い回し、送信ボタンだけ `form.submit(value="更新する")` としてラベルを変える。既存に写真が登録されている場合は、フォームの上にプレビュー表示する。

### 5. 詳細ページに更新日・編集リンクを追加する

6. `trash_map/templates/trash/detail.html` に、更新日の表示と編集ページへのリンクを追加する。
   ```html
   <p>更新日: {{ item.updated_at.strftime('%Y年%m月%d日') }}</p>
   <a href="{{ url_for('edit_page', trash_id=item.id) }}">編集する</a>
   ```
   （最初は時刻まで表示していたが、後で年月日のみの表示に変更した）

## 動作確認

1. `/trash/1` にアクセスし、更新日と「編集する」リンクが表示されることを確認する。
2. `/trash/1/edit` をGETで開き、名前・住所などが現在の値でプリフィルされ、登録済みの種別（例: `burnable`）のチェックボックスにだけ `checked` が付いていることを確認する。
3. 名前と種別（例: `burnable,can`）を変更してPOSTし、`302 /trash/1` にリダイレクトされること、DBの値が更新され、`updated_at` が自動的に新しい時刻に変わっていることを確認する。写真を再アップロードしなかった場合は、既存の写真がそのまま残っていることも確認する。
4. 確認のために一時的に変更したデータは、元の状態（名前・種別など）に戻しておく。
