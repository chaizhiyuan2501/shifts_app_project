import { defineStore } from "pinia";
import { reqStaffList, reqStaffDetail } from "@/api/staff";
import type { Staff } from "@/api/staff/type";

interface StaffState {
    staffList: Staff[];
    staffDetail: Staff | null;
}

const useStaffStore = defineStore("Staff", {
    state: (): StaffState => ({
        staffList: [],
        staffDetail: null,
    }),
    actions: {
        // スタッフ一覧を取得
        async fetchStaffList() {
            const res = await reqStaffList();
            if (res.code === 200) {
                this.staffList = res.data;
            } else {
                return Promise.reject(new Error(res.message));
            }
        },
        // スタッフ詳細を取得
        async fetchStaffDetail(id: number) {
            const res = await reqStaffDetail(id);
            if (res.code === 200) {
                this.staffDetail = res.data;
            } else {
                return Promise.reject(new Error(res.message));
            }
        },
    },
});

export default useStaffStore;
