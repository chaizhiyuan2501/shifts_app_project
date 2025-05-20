<template>
    <!-- ログイン画面全体のコンテナ -->
    <div class="login_container">
        <el-row>
            <!-- 左側の余白（PC表示時のレイアウト調整用） -->
            <el-col :span="12" :xs="0"></el-col>

            <!-- 右側のログインフォーム（モバイルでは全幅） -->
            <el-col :span="12" :xs="24">
                <el-form class="login_form">
                    <!-- タイトル部分 -->
                    <h1>ようこそ!</h1>
                    <h2>タイトルへ</h2>

                    <!-- ユーザー名の入力欄 -->
                    <el-form-item>
                        <el-input :prefix-icon="User" v-model="loginForm.username"></el-input>
                    </el-form-item>

                    <!-- パスワードの入力欄 -->
                    <el-form-item>
                        <el-input type="password" v-model="loginForm.password" :prefix-icon="Lock"
                            show-password></el-input>
                    </el-form-item>

                    <!-- ログインボタン -->
                    <el-form-item>
                        <el-button class="login_btn" type="primary" size="default">
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
import { reactive } from "vue";

// フォームの入力値（双方向バインディング用）
let loginForm = reactive({
    username: "test",  // 初期値を設定（テスト用）
    password: "pass"
});
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
