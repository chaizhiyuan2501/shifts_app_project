// ユーザーログイン用のリクエスト型
export interface UserLoginRequest {
    name: string;
    password: string;
    code: number;
}

// ログイン成功時のレスポンス型（JWTトークン + ユーザー情報）
export interface UserLoginResponse {
    access: string;
    refresh: string;
    code: number;
    token: string;
    user: {
        id: number;
        name: string;
        email: string | null;
        is_staff: boolean;
    };
}

// ユーザー情報（読み取り専用）
export interface User {
    id: number;
    name: string;
    email: string | null;
    is_staff: boolean;
    is_active: boolean;
}

// ユーザー登録用（POST専用）
export interface UserRegisterRequest {
    name: string;
    email?: string;
    password: string;
    is_staff?: boolean;
}
