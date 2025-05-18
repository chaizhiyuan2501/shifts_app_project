import request from "@/utils/request";
import type {
    MealType,
    MealOrder,
    MealOrderCount,
    MealOrderSubmitRequest
} from "./type";

export const API = {
    MEAL_TYPE_LIST: "/meal/meal-types/",
    MEAL_TYPE_DETAIL: "/meal/meal-types", // + /{id}/

    MEAL_ORDER_LIST: "/meal/meal-orders/",
    MEAL_ORDER_DETAIL: "/meal/meal-orders", // + /{id}/

    MEAL_ORDER_AUTO_GENERATE: "/meal/meal-orders/auto-generate/",
    MEAL_ORDER_COUNT: "/meal/meal-orders/count/",
    MEAL_ORDER_PERIODS: "/meal/meal-orders/stats-periods/",
} as const;

// 食事タイプ一覧取得
export const reqMealTypeList = () =>
    request.get<MealType[]>(API.MEAL_TYPE_LIST);

// 食事注文一覧取得
export const reqMealOrderList = () =>
    request.get<MealOrder[]>(API.MEAL_ORDER_LIST);

// 食事注文新規登録（ゲストまたはスタッフ）
export const reqCreateMealOrder = (data: MealOrderSubmitRequest) =>
    request.post<MealOrder>(API.MEAL_ORDER_LIST, data);

// 食事注文詳細取得
export const reqMealOrderDetail = (id: number) =>
    request.get<MealOrder>(`${API.MEAL_ORDER_DETAIL}/${id}/`);

// 食事注文更新
export const reqUpdateMealOrder = (id: number, data: MealOrderSubmitRequest) =>
    request.put<MealOrder>(`${API.MEAL_ORDER_DETAIL}/${id}/`, data);

// 食事注文削除
export const reqDeleteMealOrder = (id: number) =>
    request.delete(`${API.MEAL_ORDER_DETAIL}/${id}/`);

// 食事自動生成
export const reqMealOrderAutoGenerate = (date: string) =>
    request.post(API.MEAL_ORDER_AUTO_GENERATE, { date });

// 食事件数取得
export const reqMealOrderCount = (date: string) =>
    request.get<MealOrderCount>(API.MEAL_ORDER_COUNT, { params: { date } });

// 食事統計対象期間リスト取得
export const reqMealOrderPeriods = () =>
    request.get<string[]>(API.MEAL_ORDER_PERIODS);
