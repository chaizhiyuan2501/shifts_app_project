import request from "@/utils/request";

export const API = {
    USER_LOGIN_URL: "/user/login/",
    USER_REGISTER_URL: "/user/register/",
    USER_TOKEN_REFRESH_URL: "/user/token/refresh/",
    USER_LIST_URL: "/user/users/",
    USER_DETAIL_URL: "/user/users", // + /{id} 動的追加
} as const;

export const reqUserLogin = (data: any) => request.post(API.USER_LOGIN_URL, data);

export const reqUserDetail = (id: number) =>
    request.get(`${API.USER_DETAIL_URL}/${id}/`);