from django.apps import AppConfig
from django.db.models.signals import post_migrate


class StaffConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "staff"

    def ready(self):
        # アプリケーション起動時に signals.py をインポートして
        # post_migrate シグナル（マイグレーション後に実行される処理）を登録する。
        # これにより、DBマイグレーション完了後に初期データ（職種やシフト）を自動作成できる。
        from . import signals
