import { defineStore } from "pinia";
import { reqGuestList, reqGuestDetail } from "@/api/guest";
import type { Guest } from "@/api/guest/type";

interface GuestState {
    guestList: Guest[];
    guestDetail: Guest | null;
}

const useGuestStore = defineStore("Guest", {
    state: (): GuestState => ({
        guestList: [],
        guestDetail: null,
    }),
    actions: {
        // 利用者一覧の取得
        async fetchGuestList() {
            const res = await reqGuestList();
            if (res.code === 200) {
                this.guestList = res.data;
            } else {
                return Promise.reject(new Error(res.message));
            }
        },
        // 利用者詳細の取得
        async fetchGuestDetail(id: number) {
            const res = await reqGuestDetail(id);
            if (res.code === 200) {
                this.guestDetail = res.data;
            } else {
                return Promise.reject(new Error(res.message));
            }
        },
    },
});

export default useGuestStore;
