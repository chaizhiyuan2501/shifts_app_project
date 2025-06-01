// src/store/modules/user.ts
import { defineStore } from "pinia";
import { reqUserLogin, reqUserRegister } from "@/api/user";
import type { UserLoginRequest, UserLoginResponse, UserRegisterRequest, UserRegisterResponse } from "@/api/user/type";
import type { UserState } from "./type/type";
import { SET_TOKEN, GET_TOKEN } from "@/utils/token";

import { constantRoute } from "@/router/routes";

let useUserStore = defineStore("User", {
    state: (): UserState => {
        return {
            token: GET_TOKEN(),
            menuRoutes:constantRoute,
        }
    },
    actions: {
        // ユーザーのログイン処理を行うアクション
        async userLogin(data: UserLoginRequest) {
            let result: UserLoginResponse = await reqUserLogin(data);
            if (result.code == 200) {
                this.token = result.access as string;
                SET_TOKEN(result.access as string);
                return "ok";
            } else {
                return Promise.reject(new Error(result.data.message));
            }
        },
        // ユーザーの登録処理を行うアクション
        async userRegister(data: UserRegisterRequest) {
            let result: UserRegisterResponse = await reqUserRegister(data);
            if (result.code == 200) {
                return "ok";
            } else {
                return Promise.reject(new Error(result.message));
            }
        }
    },
    getters: {
    }
});

export default useUserStore;