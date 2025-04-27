from datetime import timedelta
from staff.models import Staff, ShiftType, WorkSchedule


def assign_night_shift(staff_id, base_date):
    """
    夜勤シフトを3日連続（夜→明→休）で自動作成する関数。

    引数:
        staff_id (int): スタッフのID
        base_date (date): 夜勤開始日

    戻り値:
        list(dict): 登録結果リスト（各日にちとシフト種別、作成有無）
    """
    staff = Staff.objects.get(id=staff_id)

    # 「夜」「明」「休」シフトの取得
    shift_map = {
        "夜": ShiftType.objects.get(code="夜"),
        "明": ShiftType.objects.get(code="明"),
        "休": ShiftType.objects.get(code="休"),
    }

    results = []
    for offset, shift_code in enumerate(["夜", "明", "休"]):
        target_date = base_date + timedelta(days=offset)
        obj, created = WorkSchedule.objects.update_or_create(
            staff=staff,
            date=target_date,
            defaults={"shift": shift_map[shift_code]},
        )
        results.append(
            {
                "date": target_date,
                "shift": shift_code,
                "created": created,
            }
        )

    return results
