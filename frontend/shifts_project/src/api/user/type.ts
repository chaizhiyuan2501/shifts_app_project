// type.ts

// ユーザーログイン用のリクエスト型
export interface UserLoginRequest {
    name: string;
    password: string;
}

// ログイン成功時のレスポンス型（JWTトークン）
export interface UserLoginResponse {
    access: string;
    refresh: string;
}

// ユーザー情報
export interface User {
    id: number;
    name: string;
    email?: string;
    is_staff: boolean;
    is_active: boolean;
}

// 新規登録用の型
export interface UserRegisterRequest {
    name: string;
    email?: string;
    password: string;
}
