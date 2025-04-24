import re
import os
import numpy as np
import cv2
from PIL import Image
from yomitoku import DocumentAnalyzer
from guest.models import Guest, VisitType, VisitSchedule

# OCR 出力文字と VisitType.name の対応辞書
VISIT_TYPE_MAPPING = {
    "泊": "泊まり",
    "通い": "通い",
    "休": "休み",
}


class ScheduleOCRProcessor:
    """
    画像から訪問スケジュールを読み取り、DBへ保存する処理クラス。
    - 画像ファイル名や画像内の文字列から利用者名・年月を抽出
    - OCR解析結果から日付と訪問種別を抽出
    - VisitSchedule モデルに保存
    """

    def __init__(self, image_path):
        """
        初期化メソッド。
        :param image_path: 処理対象の画像ファイルパス
        """
        self.image_path = image_path
        self.filename = os.path.basename(image_path)
        self.guest_name = "guest"  # 初期値として guest を設定
        self.year = "2025"  # 年の初期値
        self.month = "04"  # 月の初期値
        self.schedule = []  # 認識されたスケジュール情報リスト

    def extract_meta_from_filename(self):
        """
        ファイル名から利用者名・年月を抽出する。
        例: guest_芳賀_2025-04.png → 芳賀, 2025年4月
        """
        name_match = re.search(r"_(.+?)_", self.filename)
        date_match = re.search(r"(\d{4})[\u5e74/-]?(\d{1,2})", self.filename)

        if name_match:
            self.guest_name = name_match.group(1)
        if date_match:
            self.year = date_match.group(1)
            self.month = f"{int(date_match.group(2)):02d}"

    def analyze_image(self):
        """
        OCR処理を行い、スケジュール情報を self.schedule に格納する。
        - ファイル名と画像内から meta 情報を取得
        - 画像を RGB→BGR 変換して OCR 処理に渡す
        - 段落テキストとテーブル内データをパース
        """
        self.extract_meta_from_filename()

        image = Image.open(self.image_path).convert("RGB")
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        analyzer = DocumentAnalyzer(configs={})
        result, _, _ = analyzer(image)

        # 「様」付き名前を画像内から抽出し guest_name を上書き
        for para in result.paragraphs:
            if "様" in para.contents:
                match = re.search(r"(\S+)\s*様", para.contents)
                if match:
                    self.guest_name = match.group(1)
                    print(f"\U0001f464 画像内の名前を検出: {self.guest_name}")
                    break

        # 画像内の年月を検出して上書き
        for para in result.paragraphs:
            if re.search(r"\d{4}年\d{1,2}月", para.contents):
                match = re.search(r"(\d{4})年(\d{1,2})月", para.contents)
                if match:
                    self.year = match.group(1)
                    self.month = f"{int(match.group(2)):02d}"
                    print(f"\U0001f4c5 画像内の年月を検出: {self.year}-{self.month}")
                    break

        # テーブル内の各セルを解析し、日付と訪問種別を抽出
        print(f"\n\U0001f4dd OCR分析されたテーブル数： {len(result.tables)}")
        for table in result.tables:
            for cell in table.cells:
                content = cell.contents.strip().replace("\n", " ")
                print(f"行: {cell.row} 列: {cell.col} 内容: {content}")
                if any(key in content for key in VISIT_TYPE_MAPPING.keys()):
                    match = re.search(
                        r"(\d{1,2})\s*(" + "|".join(VISIT_TYPE_MAPPING.keys()) + r")",
                        content,
                    )
                    if match:
                        day = int(match.group(1))
                        raw_type = match.group(2)
                        visit_type = VISIT_TYPE_MAPPING.get(raw_type)
                        if visit_type:
                            self.schedule.append(
                                {
                                    "date": f"{self.year}-{self.month}-{day:02d}",
                                    "type": visit_type,
                                }
                            )

    def save_to_database(self):
        """
        認識されたスケジュール情報を DB に保存する。
        - Guest が存在しない場合は新規作成
        - VisitType に対応するスケジュールを update_or_create
        - 保存件数を返す
        """
        guest, _ = Guest.objects.get_or_create(name=self.guest_name)
        created_count = 0

        for item in self.schedule:
            date = item["date"]
            visit_type_name = item["type"]

            print(f"\U0001f4c5 保存中: {date} - {visit_type_name}")
            try:
                visit_type = VisitType.objects.get(name=visit_type_name)
            except VisitType.DoesNotExist:
                print(f"⚠️ VisitType 不存在: {visit_type_name}")
                continue

            try:
                _, created = VisitSchedule.objects.update_or_create(
                    guest=guest, date=date, defaults={"visit_type": visit_type}
                )
                if created:
                    created_count += 1
            except Exception as e:
                print(f"❌ VisitSchedule 保存失败: {e}")
                continue

        return created_count

    def run(self):
        """
        一連の処理を実行。
        :return: 保存対象者名、年月、作成件数を含む辞書
        """
        self.analyze_image()
        count = self.save_to_database()
        return {
            "guest": self.guest_name,
            "year": self.year,
            "month": self.month,
            "count": count,
        }
