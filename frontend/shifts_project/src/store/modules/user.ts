import { defineStore } from "pinia";
import { reqUserLogin } from "@/api/user";
import type { UserLoginRequest } from "@/api/user/type";

let useUserStore = defineStore("User", {
    state: () => {
        return {
            token: "",
        }
    },
    actions: {
        async userLogin(data: UserLoginRequest) {
            let result = await reqUserLogin(data);
            if (result.code == 200) {
                this.token = result.data.token;
                localStorage.setItem("TOKEN",result.data.token)
            }
        }
    },
    getters: {

    }
})

export default useUserStore;