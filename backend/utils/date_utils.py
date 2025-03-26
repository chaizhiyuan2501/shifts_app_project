

def get_weekday_jp(date):
    """
    指定した日付の曜日を日本語で返す（例：月、火、水、...）
    """
    if date is None:
        return ""
    return ["月", "火", "水", "木", "金", "土", "日"][date.weekday()]
