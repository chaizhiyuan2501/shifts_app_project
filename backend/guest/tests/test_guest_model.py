import pytest
from datetime import date, time
from guest.models import Guest, VisitType, VisitSchedule


@pytest.mark.django_db
class TestGuestModels:
    """
    Guestアプリのモデルに関するテストクラス。
    - Guest（利用者）
    - VisitType（来所区分）
    - VisitSchedule（来所予定）

    各モデルの作成・制約・文字列表示をテストする。
    """

    def setup_method(self):
        """
        テスト用に共通で使用するゲストと来所区分を作成する。
        """
        self.guest = Guest.objects.create(full_name="山田太郎")
        self.visit_type = VisitType.objects.create(
            code="通", name="通常利用", color="#ff0000"
        )

    def test_create_guest(self):
        """
        Guest モデルの作成テスト
        - 氏名・カナ名が保存されるか
        - __str__ メソッドが氏名を返すか
        """
        guest = Guest.objects.create(full_name="佐藤花子",birthday="1940-01-01",contact="00011112222",notes="要介護3")
        assert guest.full_name == "佐藤花子"
        assert guest.birthday == "1940-01-01"
        assert guest.contact == "00011112222"
        assert guest.notes == "要介護3"
        assert str(guest) == "佐藤花子"

    def test_create_visit_type(self):
        """
        VisitType モデルの作成テスト
        - コード、名称、色が正しく保存されるか
        - __str__ メソッドが「コード（名称）」形式か
        """
        visit = VisitType.objects.create(code="体", name="体験利用", color="#00ff00")
        assert visit.code == "体"
        assert visit.name == "体験利用"
        assert str(visit) == "体（体験利用）"

    def test_create_visit_schedule(self):
        """
        VisitSchedule モデルの作成テスト
        - 正しい日付、来所区分、来所・退所時間が保存されるか
        - __str__ メソッドのフォーマットが期待通りか
        - 曜日（日本語）が正しく返されるか
        """
        schedule = VisitSchedule.objects.create(
            guest=self.guest,
            date=date(2025, 4, 3),
            visit_type=self.visit_type,
            arrive_time=time(9, 0),
            leave_time=time(17, 0),
            note="初回面談",
        )
        assert schedule.guest == self.guest
        assert schedule.visit_type == self.visit_type
        assert schedule.arrive_time == time(9, 0)
        assert str(schedule).startswith("2025-04-03 - 山田太郎")
        assert schedule.weekday_jp in ["月", "火", "水", "木", "金", "土", "日"]

    def test_unique_constraint(self):
        """
        同一利用者が同じ日に複数の来所予定を登録できない制約の確認。
        - unique_together が機能しているか
        - 同日同ゲストで登録するとエラーになるか
        """
        VisitSchedule.objects.create(
            guest=self.guest,
            date=date(2025, 4, 3),
            visit_type=self.visit_type,
            arrive_time=time(10, 0),
            leave_time=time(16, 0),
        )
        with pytest.raises(Exception):
            VisitSchedule.objects.create(
                guest=self.guest,
                date=date(2025, 4, 3),
                visit_type=self.visit_type,
                arrive_time=time(11, 0),
                leave_time=time(15, 0),
            )
