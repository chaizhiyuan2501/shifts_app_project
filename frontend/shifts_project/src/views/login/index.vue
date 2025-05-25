<!-- src/views/login/index.vue -->
<template>
    <!-- ログイン画面全体のコンテナ -->
    <div class="login_container">
        <el-row>
            <!-- 左側の余白（PC表示時のレイアウト調整用） -->
            <el-col :span="12" :xs="0"></el-col>

            <!-- 右側のログインフォーム（モバイルでは全幅） -->
            <el-col :span="12" :xs="24">
                <el-form class="login_form" :model="loginForm" :rules="rules">
                    <!-- タイトル部分 -->
                    <h1>ようこそ!</h1>
                    <h2>タイトルへ</h2>

                    <!-- ユーザー名の入力欄 -->
                    <el-form-item prop="name">
                        <el-input :prefix-icon="User" v-model="loginForm.name"></el-input>
                    </el-form-item>

                    <!-- パスワードの入力欄 -->
                    <el-form-item prop="password">
                        <el-input type="password" v-model="loginForm.password" :prefix-icon="Lock"
                            show-password></el-input>
                    </el-form-item>

                    <!-- ログインボタン -->
                    <el-form-item>
                        <el-button :loading="loading" class="login_btn" type="primary" size="default" @click="login">
                            ログイン
                        </el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </div>
</template>

<script setup lang="ts">
/**
 * 使用するアイコンコンポーネントを Element Plus からインポート
 * Vue の reactive を使ってフォームのデータを定義
 */
import { User, Lock } from "@element-plus/icons-vue";
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElNotification } from "element-plus";
import useUserStore from "@/store/modules/user"
import { getTime } from "@/utils/time";

let useStore = useUserStore();
let $router = useRouter();
let loading = ref(false);
// フォームの入力値（双方向バインディング用）
let loginForm = reactive({
    name: "test",  // 初期値を設定（テスト用）
    password: "pass"
});

const login = async () => {
    loading.value = true;
    try {
        await useStore.userLogin({
            ...loginForm,
            // code:0,
        });
        $router.push("/");
        ElNotification({
            type: "success",
            message: "ゲストさん",
            title: `${(getTime())}!`
        });
        loading.value = false;
    } catch (error) {
        loading.value = false;
        ElNotification({
            type: "error",
            message: (error as Error).message
        })
    }
}

const rules = {
    name: [
        { required: true, min: 4, max: 20, message: "ユーザー名は最小4文字､最大は20文字まで", trigger: "change" },
    ],
    password: [
        { required: true, min: 4, max: 20, message: "パスワードは最小4文字､最大は20文字まで", trigger: "change" },
    ],
}
</script>

<style scoped lang="scss">
/* ログインページ全体の背景設定 */
.login_container {
    width: 100%;
    height: 100vh;
    background: url("@/assets/images/background.jpg") no-repeat;
    background-size: cover;
}

/* ログインフォームのデザイン設定 */
.login_form {
    position: relative;
    width: 80%;
    top: 30vh;
    /* 画面の縦中央に寄せる */
    background: url("@/assets/images/login_form.png") no-repeat;
    background-size: cover;
    padding: 40px;

    h1 {
        color: white;
        font-size: 40px;
    }

    h2 {
        color: white;
        font-size: 20px;
        margin: 20px 0px;
    }

    /* ログインボタンの幅をフォームと合わせる */
    .login_btn {
        width: 100%;
    }
}
</style>
