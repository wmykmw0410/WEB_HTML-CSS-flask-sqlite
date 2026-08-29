import os
import uuid

from flask import Flask, render_template, request, redirect, url_for
from geopy.geocoders import Nominatim
from werkzeug.utils import secure_filename

from constants import GARBAGE_TYPES, PREFECTURES
from form import AddGarbageForm
from models import db, TrashCan

basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(basedir, 'instance')
os.makedirs(instance_dir, exist_ok=True)

upload_dir = os.path.join(basedir, 'static', 'uploads')
os.makedirs(upload_dir, exist_ok=True)

app = Flask(__name__)
geolocator = Nominatim(user_agent="my_trash_app")
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = upload_dir
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB。写真アップロードの上限サイズ

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_dir, 'trash_cans.sqlite')
db.init_app(app)

with app.app_context():
    db.create_all()


GARBAGE_TYPE_LABELS = dict(GARBAGE_TYPES)


@app.context_processor
def inject_garbage_types():
    # base.html のハンバーガーメニューなど、どのテンプレートからでも
    # ゴミ種別一覧を参照できるようグローバルに注入する
    return {"garbage_types": GARBAGE_TYPES}


# -------------------------
# ルーティング
# -------------------------

# 地図ページ
@app.route("/map")
def map_page():
    return render_template("map/map.html")


# トップページ（地図ページと同じ内容を表示）
@app.route("/")
def index_page():
    return render_template("map/map.html")


# ゴミ箱追加ページ
@app.route("/add", methods=['GET', 'POST'])
def add_page():
    form = AddGarbageForm()
    if form.validate_on_submit():
        photo_filename = None
        if form.photo.data:
            # secure_filename で元のファイル名を無害化した上で拡張子だけ取り出し、
            # uuid で一意なファイル名を生成する（同名ファイルの衝突・パストラバーサル対策）
            ext = os.path.splitext(secure_filename(form.photo.data.filename))[1]
            photo_filename = f"{uuid.uuid4().hex}{ext}"
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        trash_can = TrashCan(
            name=form.name.data,
            postal_code=form.postal_code.data,
            prefecture=form.prefecture.data,
            city=form.city.data,
            address_line=form.address_line.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            # SelectMultipleFieldの選択値（リスト）をカンマ区切り文字列にして1カラムに保存する
            type=",".join(form.type.data),
            photo_filename=photo_filename
        )
        db.session.add(trash_can)
        db.session.commit()
        return redirect(url_for("thankyou_page"))
    return render_template("trash/add.html", form=form)


# 登録完了ページ
@app.route("/thankyou")
def thankyou_page():
    return render_template("trash/thankyou.html")


# ゴミ種別ごとの一覧ページ（都道府県・市区町村での絞り込み対応）
@app.route("/list/<type_key>")
def type_list_page(type_key):
    label = GARBAGE_TYPE_LABELS.get(type_key, type_key)
    selected_prefecture = request.args.get('prefecture', '')
    city_query = request.args.get('city', '').strip()

    # type はカンマ区切り文字列なので、部分一致ではなく
    # split したリストに対する完全一致でフィルタする。
    # 例えば "burnable" は "nonburnable" の部分文字列なので、
    # 単純な文字列検索だと不燃ごみが燃えるゴミの一覧に混入してしまう。
    items = [
        trash_can for trash_can in TrashCan.query.all()
        if type_key in trash_can.type.split(",")
    ]
    if selected_prefecture:
        items = [item for item in items if item.prefecture == selected_prefecture]
    if city_query:
        items = [item for item in items if city_query in item.city]

    return render_template(
        "trash/type_list.html",
        label=label,
        type_key=type_key,
        items=items,
        prefectures=PREFECTURES,
        selected_prefecture=selected_prefecture,
        city_query=city_query
    )


# ゴミ箱詳細ページ
@app.route("/trash/<int:trash_id>")
def detail_page(trash_id):
    trash_can = db.get_or_404(TrashCan, trash_id)
    type_labels = [GARBAGE_TYPE_LABELS.get(key, key) for key in trash_can.type.split(",")]
    return render_template("trash/detail.html", item=trash_can, type_labels=type_labels)


# ゴミ箱編集ページ
@app.route("/trash/<int:trash_id>/edit", methods=['GET', 'POST'])
def edit_page(trash_id):
    trash_can = db.get_or_404(TrashCan, trash_id)

    # obj=trash_can で渡すと、SelectMultipleField(type) が
    # DB上のカンマ区切り文字列（例: "burnable,can"）を1文字ずつ
    # 反復してしまい、チェックボックスの初期選択が壊れる。
    # そのため個別キーワード引数で渡し、type だけリストに変換して渡す。
    form = AddGarbageForm(
        name=trash_can.name,
        postal_code=trash_can.postal_code,
        prefecture=trash_can.prefecture,
        city=trash_can.city,
        address_line=trash_can.address_line,
        latitude=trash_can.latitude,
        longitude=trash_can.longitude,
        type=trash_can.type.split(",")
    )
    if form.validate_on_submit():
        trash_can.name = form.name.data
        trash_can.postal_code = form.postal_code.data
        trash_can.prefecture = form.prefecture.data
        trash_can.city = form.city.data
        trash_can.address_line = form.address_line.data
        trash_can.latitude = form.latitude.data
        trash_can.longitude = form.longitude.data
        trash_can.type = ",".join(form.type.data)
        # 写真は新しくアップロードされた場合のみ差し替え、なければ既存のものを維持する
        if form.photo.data:
            ext = os.path.splitext(secure_filename(form.photo.data.filename))[1]
            photo_filename = f"{uuid.uuid4().hex}{ext}"
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
            trash_can.photo_filename = photo_filename
        db.session.commit()
        return redirect(url_for("detail_page", trash_id=trash_can.id))
    return render_template("trash/edit.html", form=form, item=trash_can)


# 地図表示用：登録済みゴミ箱一覧API
@app.route("/api/trashcans")
def api_trashcans():
    trash_cans = TrashCan.query.all()
    return {
        "items": [
            {
                "id": trash_can.id,
                "name": trash_can.name,
                "latitude": trash_can.latitude,
                "longitude": trash_can.longitude,
            }
            for trash_can in trash_cans
        ]
    }


if __name__ == '__main__':
    app.run(debug=True)
