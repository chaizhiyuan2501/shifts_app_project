from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Role, ShiftType
import datetime


@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    """
    デフォルトの職種およびシフト種別をDBに登録するシグナル関数。
    この関数は `migrate` 実行後に自動的に呼び出される。

    - 初期職種（管理者・正社員・アルバイト・夜勤専門）を自動登録
    - よく使われるシフト（早番・夜勤・明け・休み・訪問・ケアマネ）を自動登録
    """

    # 1. 職種（Role）を初期登録
    default_roles = ["管理者", "正社員", "アルバイト", "夜勤専門"]
    for role_name in default_roles:
        # Roleテーブルに存在しない場合のみ追加
        Role.objects.get_or_create(name=role_name)

    # 2. シフト種別（ShiftType）を初期登録
    default_shifts = [
        {
            "code": "日1",  # コード（1文字〜2文字程度で省略表示用）
            "name": "日勤1",  # 表示名
            "start": "09:00",  # 勤務開始時刻
            "end": "18:00",  # 勤務終了時刻
            "color": "#2ecc71",  # 表示色（カレンダーUI用など）
        },
        {
            "code": "日2",
            "name": "日勤2",
            "start": "09:00",
            "end": "18:00",
            "color": "#2e40cc",
        },
        {
            "code": "夜",
            "name": "夜勤",
            "start": "17:00",
            "end": "00:00",
            "color": "#3498db",
        },
        {
            "code": "明",
            "name": "明け",
            "start": "00:00",
            "end": "10:00",
            "color": "#f1c40f",
        },
        {
            "code": "休",
            "name": "休み",
            "start": "00:00",
            "end": "00:00",
            "color": "#e74c3c",
        },
        {
            "code": "訪",
            "name": "訪問",
            "start": "08:30",
            "end": "17:30",
            "color": "#9b59b6",
        },
        {
            "code": "ケア",
            "name": "ケアマネ",
            "start": "09:00",
            "end": "17:00",
            "color": "#1abc9c",
        },
    ]

    for shift in default_shifts:
        # codeが既に存在しない場合のみ登録する
        obj, created = ShiftType.objects.get_or_create(
            code=shift["code"],
            defaults={
                "name": shift["name"],
                "start_time": datetime.datetime.strptime(
                    shift["start"], "%H:%M"
                ).time(),  # 文字列からtime型に変換
                "end_time": datetime.datetime.strptime(shift["end"], "%H:%M").time(),
                "color": shift["color"],
            },
        )

        # 新規作成された場合のみログ表示（migrate時に確認しやすくなる）
        if created:
            print(f"Shift '{shift['name']}' を作成しました")
