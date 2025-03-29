from django.utils.timezone import now
from datetime import timedelta, date


def get_weekday_jp(date):
    """
    指定した日付の曜日を日本語で返す（例：月、火、水、...）
    """
    if date is None:
        return ""
    return ["月", "火", "水", "木", "金", "土", "日"][date.weekday()]


from datetime import date, timedelta


def get_shift_period_range(target_date=None):
    """
    指定された日付が属する「シフト集計期間（15日〜翌月15日）」の
    開始日と終了日を求める関数。

    例:
        - 2025年3月28日 → 開始日: 3月15日, 終了日: 4月15日
        - 2025年3月2日  → 開始日: 2月15日, 終了日: 3月15日

    パラメータ:
        target_date (datetime.date): 対象日（省略時は今日の日付）

    戻り値:
        tuple(datetime.date, datetime.date): (開始日, 終了日)
    """
    if not target_date:
        # 日付が指定されていない場合は、今日の日付を使用
        target_date = date.today()

    if target_date.day >= 15:
        # 15日以降の場合：今月15日を開始日、翌月15日を終了日とする
        start = target_date.replace(day=15)
        if target_date.month == 12:
            # 12月の場合は年を繰り上げて1月
            end = date(target_date.year + 1, 1, 15)
        else:
            end = date(target_date.year, target_date.month + 1, 15)
    else:
        # 15日未満の場合：前月15日を開始日、今月15日を終了日とする
        if target_date.month == 1:
            # 1月の場合は年を繰り下げて前の年の12月
            start = date(target_date.year - 1, 12, 15)
        else:
            start = date(target_date.year, target_date.month - 1, 15)
        end = target_date.replace(day=15)

    return start, end

