from django.urls import path
from .views import (
    GuestListCreateView,
    GuestDetailView,
    VisitTypeListCreateView,
    VisitTypeDetailView,
    VisitScheduleListCreateView,
    VisitScheduleDetailView,
    ScheduleUploadView,
)

app_name = "guest"

# =============================
# guest アプリの URL ルーティング定義
# =============================
# 各 URL に対して対応するビューをマッピングし、
# 管理対象となるエンドポイントを定義

urlpatterns = [
    # 利用者（Guest）API
    path(
        "guests/",
        GuestListCreateView.as_view(),
        name="guest-list-create",  # GET: 一覧取得, POST: 新規作成
    ),
    path(
        "guests/<int:pk>/",
        GuestDetailView.as_view(),
        name="guest-detail",  # GET: 取得, PUT: 更新, DELETE: 削除
    ),
    # 来訪種別（VisitType）API
    path(
        "visit-types/",
        VisitTypeListCreateView.as_view(),
        name="visit-type-list-create",  # GET: 一覧取得, POST: 新規登録
    ),
    path(
        "visit-types/<int:pk>/",
        VisitTypeDetailView.as_view(),
        name="visit-type-detail",  # GET: 詳細取得, PUT: 更新, DELETE: 削除
    ),
    # 来訪スケジュール（VisitSchedule）API
    path(
        "schedules/",
        VisitScheduleListCreateView.as_view(),
        name="schedule-list-create",  # GET: 一覧取得, POST: 登録
    ),
    path(
        "schedules/<int:pk>/",
        VisitScheduleDetailView.as_view(),
        name="schedule-detail",  # GET: 詳細, PUT: 更新, DELETE: 削除
    ),
    # OCR画像アップロード（スケジュール登録）
    path(
        "schedule-uploads/",
        ScheduleUploadView.as_view(),
        name="schedule-upload",  # POST: OCRによるスケジュール一括登録
    ),
]
