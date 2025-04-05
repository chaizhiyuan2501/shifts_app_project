from rest_framework.response import Response
from rest_framework import status


def api_response(code=status.HTTP_200_OK, message="OK", data=None, status_code=None):
    """
    統一された API レスポンス形式を返すヘルパー関数。

    Parameters:
        status_code or code (int): HTTPステータスコード（例：200, 400, 401）
        message (str): メッセージ（例："OK", "バリデーションエラー"）
        data (dict or None): 返すデータ本体

    Returns:
        rest_framework.response.Response:
            JSON形式の統一レスポンス
    """
    return Response(
        {
            "code": code,
            "message": message,
            "data": data,
        },
        status=status_code or code,
    )
