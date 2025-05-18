import request from "@/utils/request";
import type {
    ShiftType,
    Role,
    Staff,
    StaffSubmitRequest,
    WorkSchedule,
    WorkScheduleSubmitRequest,
} from "./type";

export const API = {
    SHIFT_TYPE_LIST: "/staff/shift-types/",
    SHIFT_TYPE_DETAIL: "/staff/shift-types", // + /{id}/

    ROLE_LIST: "/staff/roles/",
    ROLE_DETAIL: "/staff/roles", // + /{id}/

    STAFF_LIST: "/staff/staffs/",
    STAFF_DETAIL: "/staff/staffs", // + /{id}/

    SCHEDULE_LIST: "/staff/schedules/",
    SCHEDULE_DETAIL: "/staff/schedules", // + /{id}/",
} as const;

// シフトタイプ一覧
export const reqShiftTypeList = () => request.get<ShiftType[]>(API.SHIFT_TYPE_LIST);

// 役職一覧
export const reqRoleList = () => request.get<Role[]>(API.ROLE_LIST);

// スタッフ一覧
export const reqStaffList = () => request.get<Staff[]>(API.STAFF_LIST);

// スタッフ新規登録
export const reqCreateStaff = (data: StaffSubmitRequest) =>
    request.post<Staff>(API.STAFF_LIST, data);

// スタッフ詳細取得
export const reqStaffDetail = (id: number) =>
    request.get<Staff>(`${API.STAFF_DETAIL}/${id}/`);

// 勤務スケジュール一覧
export const reqWorkScheduleList = () =>
    request.get<WorkSchedule[]>(API.SCHEDULE_LIST);

// 勤務スケジュール新規登録
export const reqCreateWorkSchedule = (data: WorkScheduleSubmitRequest) =>
    request.post<WorkSchedule>(API.SCHEDULE_LIST, data);

// 勤務スケジュール詳細取得
export const reqWorkScheduleDetail = (id: number) =>
    request.get<WorkSchedule>(`${API.SCHEDULE_DETAIL}/${id}/`);

// 勤務スケジュール更新
export const reqUpdateWorkSchedule = (id: number, data: WorkScheduleSubmitRequest) =>
    request.put<WorkSchedule>(`${API.SCHEDULE_DETAIL}/${id}/`, data);

// 勤務スケジュール削除
export const reqDeleteWorkSchedule = (id: number) =>
    request.delete(`${API.SCHEDULE_DETAIL}/${id}/`);
