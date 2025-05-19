<template>
    <div class="login_container">
        <el-row>
            <el-col :span="12" :xs="0"></el-col>
            <el-col :span="12" :xs="24">
                <el-form class="login_form">
                    <h1>ようこそ!</h1>
                    <h2>タイトルへ</h2>
                    <el-form-item>
                        <el-input></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-input type="password"></el-input>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </div>
</template>

<script setup lang="ts">

</script>

<style scoped lang="scss">
.login_container {
    width: 100%;
    height: 100vh;
    background: url("@/assets/images/background.jpg") no-repeat;
    background-size: cover;
}

.login_form {
    position: relative;
    width: 80%;
    top: 30vh;
    // background: url("@/assets/images/background.jpg") no-repeat;
    // background-size: cover;
}
</style>
