// src/store/modules/user.ts
import { defineStore } from "pinia";
import { reqUserLogin } from "@/api/user";
import type { UserLoginRequest, UserLoginResponse } from "@/api/user/type";
import type { UserState } from "./type/type";
import { SET_TOKEN, GET_TOKEN } from "@/utils/token";
let useUserStore = defineStore("User", {
    state: (): UserState => {
        return {
            token: GET_TOKEN()
        }
    },
    actions: {
        async userLogin(data: UserLoginRequest) {
            let result: UserLoginResponse = await reqUserLogin(data);
            if (result.code == 200) {
                this.token = (result.access as string);
                SET_TOKEN((result.access as string))
                return "ok";
            } else {
                return Promise.reject(new Error(result.data.message));
            }
        }
    },
    getters: {

    }
})

export default useUserStore;