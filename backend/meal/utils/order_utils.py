from datetime import date
from guest.models import Guest, VisitSchedule
from staff.models import WorkSchedule
from meal.models import MealType, MealOrder


def generate_meal_orders_for_day(target_date: date):
    """
    指定された日付に対する食事注文を自動生成する関数。

    【対象】
    - スタッフ：日勤シフトには「昼」、夜勤シフトには「夕」の注文を自動作成
    - 利用者：訪問種別が「泊」の場合、「朝・昼・夕」すべての注文を自動作成

    【非対象】
    - 利用者の訪問種別が「通い」「休」などの場合は生成対象外

    Parameters:
        target_date (date): 注文を生成する対象日付

    Returns:
        None（副作用として MealOrder を作成）
    """

    # --- 食事タイプの取得（朝・昼・夕） ---
    meal_morning = MealType.objects.get(name="朝")
    meal_lunch = MealType.objects.get(name="昼")
    meal_dinner = MealType.objects.get(name="夕")

    # --- スタッフのシフトに基づく食事自動作成 ---
    staff_schedules = WorkSchedule.objects.filter(date=target_date)

    for schedule in staff_schedules:
        if schedule.shift.code == "日":  # 日勤スタッフには昼食
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal_lunch,
                staff=schedule.staff,
                defaults={"auto_generated": True, "ordered": True},
            )
        elif schedule.shift.code == "夜":  # 夜勤スタッフには夕食
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal_dinner,
                staff=schedule.staff,
                defaults={"auto_generated": True, "ordered": True},
            )

    # --- 「泊」の利用者に対する三食の自動作成 ---
    guest_visits = VisitSchedule.objects.filter(date=target_date, visit_type__code="泊")

    for visit in guest_visits:
        guest = visit.guest
        for meal in [meal_morning, meal_lunch, meal_dinner]:
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal,
                guest=guest,
                defaults={"auto_generated": True, "ordered": True},
            )
