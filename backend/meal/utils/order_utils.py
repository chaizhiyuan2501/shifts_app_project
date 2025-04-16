from datetime import date
from guest.models import Guest, VisitSchedule
from staff.models import WorkSchedule
from meal.models import MealType, MealOrder


def generate_meal_orders_for_day(target_date: date):
    """指定された日付の食事注文を自動生成する"""

    meal_morning = MealType.objects.get(name="朝")
    meal_lunch = MealType.objects.get(name="昼")
    meal_dinner = MealType.objects.get(name="夕")

    # --- スタッフの食事処理 ---
    staff_schedules = WorkSchedule.objects.filter(date=target_date)

    for schedule in staff_schedules:
        if schedule.shift.code == "日":
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal_lunch,
                staff=schedule.staff,
                defaults={"auto_generated": True, "ordered": True},
            )
        elif schedule.shift.code == "夜":
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal_dinner,
                staff=schedule.staff,
                defaults={"auto_generated": True, "ordered": True},
            )

    # --- 患者の食事処理 ---
    guest_visits = VisitSchedule.objects.filter(date=target_date)

    for visit in guest_visits:
        guest = visit.guest
        if visit.visit_type.code == "泊":
            for meal in [meal_morning, meal_lunch, meal_dinner]:
                MealOrder.objects.update_or_create(
                    date=target_date,
                    meal_type=meal,
                    guest=guest,
                    defaults={"auto_generated": True, "ordered": True},
                )
        elif visit.visit_type.code == "通い":
            # ここに来所・帰宅時間の判定が必要
            if hasattr(visit, "arrive_time") and visit.arrive_time and visit.arrive_time.hour < 10:
                MealOrder.objects.update_or_create(
                    date=target_date,
                    meal_type=meal_morning,
                    guest=guest,
                    defaults={"auto_generated": True, "ordered": True},
                )
            MealOrder.objects.update_or_create(
                date=target_date,
                meal_type=meal_lunch,
                guest=guest,
                defaults={"auto_generated": True, "ordered": True},
            )
            if hasattr(visit, "leave_time") and visit.leave_time and visit.leave_time.hour > 17:
                MealOrder.objects.update_or_create(
                    date=target_date,
                    meal_type=meal_dinner,
                    guest=guest,
                    defaults={"auto_generated": True, "ordered": True},
                )
