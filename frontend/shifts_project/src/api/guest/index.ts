import request from "@/utils/request";
import type {
    Guest,
    GuestSubmitRequest,
    VisitSchedule,
    VisitScheduleSubmitRequest,
    VisitType
} from "./type";

export const API = {
    GUEST_LIST: "/guest/guests/",
    GUEST_DETAIL: "/guest/guests", // + /{id}/
    SCHEDULE_LIST: "/guest/schedules/",
    SCHEDULE_DETAIL: "/guest/schedules", // + /{id}/
    VISIT_TYPE_LIST: "/guest/visit-types/",
    VISIT_TYPE_DETAIL: "/guest/visit-types", // + /{id}/
    SCHEDULE_UPLOAD: "/guest/schedule-uploads/",
} as const;

// ゲスト一覧取得
export const reqGuestList = () => request.get<Guest[]>(API.GUEST_LIST);

// ゲスト詳細取得
export const reqGuestDetail = (id: number) =>
    request.get<Guest>(`${API.GUEST_DETAIL}/${id}/`);

// ゲスト新規登録
export const reqCreateGuest = (data: GuestSubmitRequest) =>
    request.post<Guest>(API.GUEST_LIST, data);

// ゲスト更新
export const reqUpdateGuest = (id: number, data: GuestSubmitRequest) =>
    request.put<Guest>(`${API.GUEST_DETAIL}/${id}/`, data);

// ゲスト削除
export const reqDeleteGuest = (id: number) =>
    request.delete(`${API.GUEST_DETAIL}/${id}/`);

// スケジュール一覧取得
export const reqScheduleList = () =>
    request.get<VisitSchedule[]>(API.SCHEDULE_LIST);

// スケジュール詳細取得
export const reqScheduleDetail = (id: number) =>
    request.get<VisitSchedule>(`${API.SCHEDULE_DETAIL}/${id}/`);

// スケジュール新規登録
export const reqCreateSchedule = (data: VisitScheduleSubmitRequest) =>
    request.post<VisitSchedule>(API.SCHEDULE_LIST, data);

// スケジュール更新
export const reqUpdateSchedule = (id: number, data: VisitScheduleSubmitRequest) =>
    request.put<VisitSchedule>(`${API.SCHEDULE_DETAIL}/${id}/`, data);

// スケジュール削除
export const reqDeleteSchedule = (id: number) =>
    request.delete(`${API.SCHEDULE_DETAIL}/${id}/`);

// スケジュール画像アップロード
export const reqScheduleUpload = (formData: FormData) =>
    request.post(API.SCHEDULE_UPLOAD, formData);

// 訪問タイプ一覧取得
export const reqVisitTypeList = () => request.get<VisitType[]>(API.VISIT_TYPE_LIST);
