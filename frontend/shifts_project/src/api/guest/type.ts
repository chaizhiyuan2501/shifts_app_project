// ゲスト情報（読み取り用）
export interface Guest {
    id: number;
    name: string;
    birthday?: string | null;
    contact?: string;
    notes?: string | null;
}

// ゲスト登録・編集用
export interface GuestSubmitRequest {
    name: string;
    birthday?: string;
    contact?: string;
    notes?: string;
}

// 訪問タイプ
export interface VisitType {
    id: number;
    name: string;
    code: string;
    color: string;
}

// 訪問スケジュール（読み取り用）
export interface VisitSchedule {
    id: number;
    guest: Guest; // ネスト
    visit_type: VisitType;
    date: string;
    arrive_time?: string | null;
    leave_time?: string | null;
    note?: string;
    weekday: string;
    needs_breakfast?: boolean;
    needs_lunch?: boolean;
    needs_dinner?: boolean;
    meal_note?: string | null;
}

// 訪問スケジュール登録・更新用
export interface VisitScheduleSubmitRequest {
    guest_id: number;
    visit_type_id: number;
    date: string;
    arrive_time?: string;
    leave_time?: string;
    note?: string;
    needs_breakfast?: boolean;
    needs_lunch?: boolean;
    needs_dinner?: boolean;
    meal_note?: string;
}
