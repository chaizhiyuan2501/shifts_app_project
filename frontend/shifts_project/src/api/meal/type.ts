// meal/type.ts

export interface MealType {
    id: number;
    name: string;
    display_name: string;
}

export interface MealOrder {
    id: number;
    date: string;
    meal_type: MealType;
    meal_type_id: number;
    guest?: number | null;
    guest_id?: number | null;
    staff?: number | null;
    staff_id?: number | null;
    ordered: boolean;
    auto_generated: boolean;
    note?: string | null;
    weekday: string;
}

export interface MealOrderSubmitRequest {
    date: string;
    meal_type_id: number;
    guest_id?: number;
    staff_id?: number;
    note?: string;
}

export interface MealOrderCount {
    朝食: number;
    昼食: number;
    夕食: number;
}
