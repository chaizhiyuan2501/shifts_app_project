
# 護工出勤管理システム

この `user` アプリは、護工出勤管理システムにおけるユーザーの登録・ログイン・管理機能を提供するモジュールです。名前と生年月日（4桁）によるログインに対応し、一般ユーザーと管理者を区別して扱うことが可能です。

---

## 🔧 主な機能

-


---

## 📦 使用技術・ライブラリ

- Python 3.11 / Django 4.2
- Django REST Framework
- djangorestframework-simplejwt
- drf-spectacular（APIドキュメント自動生成）


---

## 🔐 認証・認可

- 認証方式：JWT（`djangorestframework-simplejwt`）
- ログインには `name`（名前）と `password`（パスワード）を使用
- `is_admin=True` で管理者判定され、初期管理者アカウントはマイグレーション後に自動生成

---

## 🔌 API エンドポイント一覧（`urls.py`）

| メソッド | パス | 概要 |
|---------|------|------|
| POST | `/api/user/register/` | ユーザー登録（認証不要） |
| POST | `/api/user/login/` | JWTログイン（アクセストークン＋リフレッシュトークン） |
| POST | `/api/user/token/refresh/` | アクセストークン再発行 |
| GET | `/api/user/users/` | ユーザー一覧取得（認証必要） |
| GET | `/api/user/users/<int:id>/` | ユーザー詳細取得（認証必要） |
| PUT | `/api/user/users/<int:id>/` | ユーザー更新（認証必要） |
| DELETE | `/api/user/users/<int:id>/` | ユーザー削除（認証必要） |

---

## 🧰 補助モジュール

### `serializers.py`

- `RegisterUserSerializer`: 登録バリデーション（名前重複、メール重複、パスワード強度）
- `UserSerializer`: ユーザー情報表示・更新
- `CustomTokenObtainPairSerializer`: JWTログイン時にユーザー情報も含める

### `views.py`

- `UserRegisterView`: 登録処理
- `UserListView`, `UserDetailView`: 一覧・個別情報取得、編集、削除
- `CustomTokenObtainPairView`, `CustomTokenRefreshView`: JWT関連

### `signals.py`

- 初回マイグレーション時に以下の管理者アカウントを自動作成：
  - 名前：`admin`
  - パスワード：`1993`
  - メール：`admin@mail.com`

### `api_response_utils.py`

- レスポンス形式を以下のように統一：

```json
{
  "code": 200,
  "message": "OK",
  "data": {...}
}
```

---

## ⚙️ 環境・設定

- `AUTH_USER_MODEL = "user.User"` によりカスタムユーザーモデルを指定
- `DEFAULT_AUTHENTICATION_CLASSES` に JWT を設定済み
- `drf-spectacular` により Swagger ドキュメント生成に対応



## 📝 今後の拡張例

- パスワードリセット機能
- 一般ユーザーのプロフィール画面
- グループ・権限ベースのアクセス制御

---

## 🧑‍💻 開発者向け補足



---

