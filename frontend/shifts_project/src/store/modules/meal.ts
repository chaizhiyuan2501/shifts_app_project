import { defineStore } from "pinia";
import { reqMealOrders } from "@/api/meal";
import type { MealOrder } from "@/api/meal/type";

interface MealState {
    mealOrders: MealOrder[];
}

const useMealStore = defineStore("Meal", {
    state: (): MealState => ({
        mealOrders: [],
    }),
    actions: {
        // 食事注文一覧を取得
        async fetchMealOrders() {
            const res = await reqMealOrders();
            if (res.code === 200) {
                this.mealOrders = res.data;
            } else {
                return Promise.reject(new Error(res.message));
            }
        },
    },
});

export default useMealStore;
