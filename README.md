# 介護士シフト・食事・訪問管理システム | Django REST API + OCR + JWT


## 概要

介護士の日々のシフト管理、利用者の訪問予定、食事手配の煩雑さを軽減するために、本プロジェクトではこれらを一元管理できるAPIシステムを開発しました。



## 技術スタック

### バックエンド
- Python 3.11
- Django 4.2
- Django REST Framework
- JWT (djangorestframework-simplejwt)
- yomitoku
- SQLite（ローカル開発用）
- Docker / Docker Compose（開発・本番環境の構築用）

### フロントエンド
- Vue 3
- TypeScript
- Pinia（状態管理）
- Vue Router
- Axios
- SCSS

## 主な機能

- 管理者と一般ユーザーのログイン・認証（JWT）
- 職員の出勤・シフト情報の管理（15日〜翌月15日）
- 利用者の訪問日程（OCRによる画像解析入力をサポート）
- 食事の注文・集計（勤務種別・訪問種別に応じた自動計算、例：夜勤職員は夕食が自動付与）
- APIレスポンスの統一（`api_response` ヘルパー関数）
- テストカバレッジ100%、pytestを使用した単体・統合テスト
- Swagger UI による API ドキュメント自動生成


## 開発環境構築方法（ローカル）

```bash
git clone https://github.com/yourname/shift-management-api.git
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```


## Docker での起動方法

```bash
docker-compose up --build
docker-compose run --rm backend bash
python manage.py runserver
```


## テスト実行方法

```bash
pytest
```

## APIドキュメント（Swagger）

http://127.0.0.1:8000/api/docs/swagger/#/

※ JWTトークンを用いて認証付きAPIも試せます

### JWTトークン取得例

以下のエンドポイントにPOSTすることでトークンを取得できます。

`POST /api/user/token/`

リクエストボディ例:
```json
{
  "name": "admin",
  "password": "your_password"
}
```

```レスポンス
{
  "access": "xxxxx",
  "refresh": "yyyyy"
}
```

## ディレクトリ構成
<pre>
├── .pytest_cache
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── README.md
│   ├── v
│   │   ├── cache
│   │   │   ├── nodeids
│   │   │   ├── stepwise
├── backend
│   ├── .pytest_cache
│   │   ├── .gitignore
│   │   ├── CACHEDIR.TAG
│   │   ├── README.md
│   │   ├── v
│   │   │   ├── cache
│   │   │   │   ├── lastfailed
│   │   │   │   ├── nodeids
│   │   │   │   ├── stepwise
│   ├── db.sqlite3
│   ├── Dockerfile
│   ├── fixtures
│   │   ├── staff_shifts.json
│   ├── guest
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── tests
│   │   │   ├── test_guest_model.py
│   │   │   ├── test_guest_serializers.py
│   │   │   ├── test_guest_views.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils
│   │   │   ├── ocr_utils.py
│   │   ├── views.py
│   │   ├── __init__.py
│   ├── manage.py
│   ├── meal
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── tests
│   │   │   ├── test_meal_model.py
│   │   │   ├── test_meal_serializers.py
│   │   │   ├── test_meal_views.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils
│   │   │   ├── order_utils.py
│   │   ├── utils.py
│   │   ├── views.py
│   │   ├── __init__.py
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── shifts_project
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── settings.cpython-311.pyc
│   │   │   ├── __init__.cpython-311.pyc
│   ├── staff
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── tests
│   │   │   ├── test_staff_model.py
│   │   │   ├── test_staff_serializers.py
│   │   │   ├── test_staff_views.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── __init__.py
│   ├── user
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── tests
│   │   │   ├── test_user_models.py
│   │   │   ├── test_user_serializers.py
│   │   │   ├── test_user_view.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── __init__.py
│   ├── utils
│   │   ├── api_response_utils.py
│   │   ├── date_utils.py
│   │   ├── model_utils.py
│   │   ├── test_utils.py
├── command.md
├── docker-compose.yml
├── frontend
│   ├── Dockerfile
│   ├── node_modules
├── README.md
├── show_tree.py
├── Todo.md
</pre>


## 今後の課題
- 本番環境へのデプロイ（Render または Railway）
- フロントエンド(Vue.js)との統合（現在はAPIのみ）
- OCR機能を拡張し、職員の出勤予定も画像から読み取って登録可能にする予定


## 作者情報

- 名前：Chai Zhiyuan（サイ チゲン）
- GitHub：https://github.com/chaizhiyuan2501
- Email：chaizhiyuan2501@gmail.com