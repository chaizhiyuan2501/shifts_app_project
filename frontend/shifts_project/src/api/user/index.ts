// index.ts
import request from "@/utils/request";
import type{
  UserLoginRequest,
  UserLoginResponse,
  User,
  UserRegisterRequest
} from "@/api/user/type";

export const API = {
  USER_LOGIN_URL: "/user/login/",
  USER_REGISTER_URL: "/user/register/",
  USER_TOKEN_REFRESH_URL: "/user/token/refresh/",
  USER_LIST_URL: "/user/users/",
  USER_DETAIL_URL: "/user/users", // + /{id}/
} as const;

// ユーザーログイン
export const reqUserLogin = (data: UserLoginRequest) =>
  request.post<UserLoginResponse>(API.USER_LOGIN_URL, data);

// ユーザー一覧取得
export const reqUserList = () =>
  request.get<User[]>(API.USER_LIST_URL);

// ユーザー詳細取得（id 指定）
export const reqUserDetail = (id: number) =>
  request.get<User>(`${API.USER_DETAIL_URL}/${id}/`);

// ユーザー新規登録
export const reqUserRegister = (data: UserRegisterRequest) =>
  request.post<User>(API.USER_REGISTER_URL, data);
