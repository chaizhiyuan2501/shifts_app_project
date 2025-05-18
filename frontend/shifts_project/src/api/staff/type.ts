// シフトタイプ
export interface ShiftType {
    id: number;
    code: string;
    name: string;
    start_time: string;
    end_time: string;
    break_minutes: number;
    work_hours: number;
    color: string;
}

// 役職
export interface Role {
    id: number;
    name: string;
}

// スタッフ情報（読み取り時用）
export interface Staff {
    id: number;
    name: string;
    role: Role;        // roleはネスト表示
    notes?: string;
}

// スタッフ登録・編集用（POST/PUT用）
export interface StaffSubmitRequest {
    name: string;
    role_id: number;
    notes?: string;
}

// 勤務スケジュール（読み取り時）
export interface WorkSchedule {
    id: number;
    staff: Staff;
    shift: ShiftType;
    date: string;
    note?: string;
    weekday: string;
    needs_breakfast?: boolean;
    needs_lunch?: boolean;
    needs_dinner?: boolean;
    meal_note?: string | null;
}

// 勤務スケジュール登録・更新用
export interface WorkScheduleSubmitRequest {
    staff_id: number;
    shift_id: number;
    date: string;
    note?: string;
    needs_breakfast?: boolean;
    needs_lunch?: boolean;
    needs_dinner?: boolean;
    meal_note?: string;
}
