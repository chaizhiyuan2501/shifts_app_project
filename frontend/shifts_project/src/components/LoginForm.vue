<template>
    <form @submit.prevent="login">
        <label>名前:
            <input v-model="name" type="text" />
        </label>
        <label>パスワード（誕生日）:
            <input v-model="password" type="password" />
        </label>
        <button type="submit">ログイン</button>
    </form>
</template>

<script setup lang="ts">
import { ref } from "vue";
import request from "../utils/request";
const name = ref("");
const password = ref("");

const login = async () => {
    try {
        const res = await request.post("/user/login/", {
            name: name.value,
            password: password.value,
        });

        localStorage.setItem("access_token", res.data.access);
        localStorage.setItem("refresh_token", res.data.refresh);

        alert("ログイン成功！");

        // 登录后请求用户列表
        const userList = await request.get("/user/users/");
        console.log("ユーザー一覧:", userList.data);

    } catch (err: any) {
        console.error("ログイン失敗:", err);
        alert("ログインに失敗しました");
    }
};
</script>
