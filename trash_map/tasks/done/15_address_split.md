# 住所を都道府県・市区町村・番地に分割

日付: 2026-08-29

## これは何をする作業か

それまで「住所」は1つの自由入力欄（`address`）だった。これを「都道府県」「市区町村」「番地・建物名」の3つに分け、都道府県・市区町村で絞り込み検索ができるようにする。あわせて、郵便番号を入力すると住所が自動入力される機能も追加する。

## 手順

### 1. DBのスキーマを移行する

1. `trash_cans` テーブルに新しいカラムを追加する（既存のテーブルなので `ALTER TABLE` で追加する）。
   ```sql
   ALTER TABLE trash_cans ADD COLUMN prefecture VARCHAR(10);
   ALTER TABLE trash_cans ADD COLUMN city VARCHAR(50);
   ALTER TABLE trash_cans ADD COLUMN address_line VARCHAR(200);
   ```
2. 既存のサンプル行（id=1、住所は `"東京都千代田区丸の内1丁目"` という1つの文字列だった）を、手動で3つのカラムに分けて書き込む（バックフィル）。
   ```sql
   UPDATE trash_cans SET prefecture='東京都', city='千代田区', address_line='丸の内1丁目' WHERE id=1;
   ```
3. 古い `address` カラムはもう使わないので削除する。
   ```sql
   ALTER TABLE trash_cans DROP COLUMN address;
   ```
   - `DROP COLUMN`（カラムの削除）はデータが失われる可能性がある操作のため、実行前に必ずバックフィルが終わっていることを確認し、ユーザーに確認を取ってから実行した。
   - SQLiteのバージョンによっては `DROP COLUMN` に対応していないことがあるため、事前にバージョン（このときは3.51）を確認してから実行した。

### 2. 都道府県の一覧を定数として用意する

4. `trash_map/constants.py` に、47都道府県の一覧を追加する。
   ```python
   PREFECTURES = ["北海道", "青森県", ..., "沖縄県"]
   ```
   並び順はアルファベット順ではなく、北海道から沖縄県までの一般的な並び（JISの都道府県コード順）にする。

### 3. モデルとフォームを更新する

5. `trash_map/models.py` の `address` を削除し、代わりに `prefecture`・`city`・`address_line`（いずれも `nullable=False`）を追加する。3つを結合して住所全体を返す `full_address` というプロパティも追加する。
   ```python
   @property
   def full_address(self):
       return f"{self.prefecture}{self.city}{self.address_line}"
   ```
   こうしておけば、テンプレート側では `item.full_address` と書くだけで住所全体を表示できる。
6. `trash_map/form.py` の `address` フィールドを削除し、代わりに `prefecture`（都道府県の選択式、`SelectField`、必須）、`city`（`StringField`、必須）、`address_line`（`StringField`、必須）を追加する。フィールドの並び順は「郵便番号 → 都道府県 → 市区町村 → 番地」とし、次の自動補完機能の入力の流れに合わせる。

### 4. 一覧ページに絞り込み機能を追加する

7. `trash_map/app.py` の `type_list_page` に、クエリパラメータでの絞り込みを追加する。
   ```python
   selected_prefecture = request.args.get('prefecture', '')
   city_query = request.args.get('city', '').strip()
   if selected_prefecture:
       items = [item for item in items if item.prefecture == selected_prefecture]
   if city_query:
       items = [item for item in items if city_query in item.city]
   ```
   都道府県は完全一致、市区町村は部分一致で絞り込む。
8. `trash_map/templates/trash/type_list.html` に、都道府県セレクト（全47都道府県＋「すべて」）と市区町村のテキスト入力からなる絞り込みフォームを追加する。`method="get"` にすることで、絞り込み条件がURLのクエリパラメータとして残り、ページ再読み込みや共有がしやすくなる。「クリア」リンクで絞り込みなしの状態に戻せるようにする。

### 5. 郵便番号からの住所自動補完を実装する

9. `trash_map/static/js/postal_lookup.js` を新規作成する。郵便番号の入力欄からフォーカスが外れた（`blur`）タイミングで、入力値が7桁の数字であれば外部の郵便番号検索API（`https://zipcloud.ibsnet.co.jp/api/search`）に問い合わせる。このAPIはAPIキーが不要で、CORS（別ドメインからのアクセス許可）にも対応した無料の公開APIのため、ブラウザから直接呼び出せる。
   ```javascript
   fetch(`https://zipcloud.ibsnet.co.jp/api/search?zipcode=${digits}`)
       .then(response => response.json())
       .then(data => {
           const result = data.results[0];
           prefectureSelect.value = result.address1;
           cityInput.value = result.address2;
           addressLineInput.value = result.address3;
       });
   ```
   通信エラーやAPI側の不具合で取得に失敗した場合は、何もせず手入力に任せる（エラーでフォーム自体が壊れないようにする）。
10. `trash_map/templates/trash/add.html` と `trash_map/templates/trash/edit.html` に、このスクリプトを読み込む `<script>` タグを追加する。

## 動作確認

1. 郵便番号「530-0001」を指定して新規登録し、都道府県「大阪府」・市区町村「大阪市北区」・番地「梅田1丁目」として正しくDBに保存され、`full_address` で結合表示されることを確認する（自動補完はブラウザ専用の機能なので、確認時はフォームの値を直接指定して送信した）。
2. `/list/glass?prefecture=大阪府` で該当データが表示され、`/list/glass?prefecture=東京都` では表示されないことを確認する（絞り込みロジックの検証）。
3. 確認用に登録したテストレコードはDBから削除しておく。
4. 郵便番号自動補完（外部API呼び出し）自体は、実際のブラウザでの手動確認が必要（自動テストの環境では外部APIへの実際の通信までは検証できない）。
