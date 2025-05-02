from datetime import date
from guest.models import VisitSchedule
from staff.models import WorkSchedule
from meal.models import MealType, MealOrder


def generate_meal_orders_for_day(target_date: date):
    """
    新ロジック：指定された日付に対して、勤務・来所スケジュールから
    needs_breakfast / needs_lunch / needs_dinner をもとに MealOrder を生成する。

    Parameters:
        target_date (date): 注文を生成する対象日付
    """

    # 食事タイプの取得（name="朝" "昼" "夕"）
    meal_type_map = {mt.name: mt for mt in MealType.objects.all()}

    # ========================
    # スタッフ分の注文生成
    # ========================
    staff_schedules = WorkSchedule.objects.filter(date=target_date)

    for schedule in staff_schedules:
        if schedule.needs_breakfast:
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal_type_map["朝"],
                staff=schedule.staff,
                defaults={"auto_generated": True, "ordered": True},
            )
        if schedule.needs_lunch:
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal_type_map["昼"],
                staff=schedule.staff,
                defaults={"auto_generated": True, "ordered": True},
            )
        if schedule.needs_dinner:
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal_type_map["夕"],
                staff=schedule.staff,
                defaults={"auto_generated": True, "ordered": True},
            )

    # ========================
    # 利用者分の注文生成
    # ========================
    guest_schedules = VisitSchedule.objects.filter(date=target_date)

    for schedule in guest_schedules:
        if schedule.needs_breakfast:
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal_type_map["朝"],
                guest=schedule.guest,
                defaults={"auto_generated": True, "ordered": True},
            )
        if schedule.needs_lunch:
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal_type_map["昼"],
                guest=schedule.guest,
                defaults={"auto_generated": True, "ordered": True},
            )
        if schedule.needs_dinner:
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal_type_map["夕"],
                guest=schedule.guest,
                defaults={"auto_generated": True, "ordered": True},
            )
