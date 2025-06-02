<template>
    <div class="layout_container">
        <!-- 左側サイドメニュー -->
        <div class="layout_slider">
            <Logo></Logo>
            <el-scrollbar class="scrollbar">
                <el-menu background-color="#001529" text-color="white">
                    <Menu :menuList="userStore.meRoutes"></Menu>
                </el-menu>
            </el-scrollbar>
        </div>
        <!-- トップナビゲーションバー -->
        <div class="layout_tabbar">トップナビゲーション</div>
        <!-- コンテンツ表示エリア -->
        <div class="layout_main">コンテンツ表示エリア</div>
    </div>
</template>
<script setup lang="ts">
import Logo from "./logo/index.vue"
import Menu from "./menu/index.vue"
import useUserStore from "@/store/modules/user"

let userStore = useUserStore();
</script>
<style scoped lang="scss">
.layout_container {
    width: 100%;
    height: 100vh;
    background: red;

    .layout_slider {
        width: $base-menu-width;
        height: 100vh;
        background: $base-menu-background-color;

        .scrollbar {
            width: 100%;
            height: calc(100vh-$base-menu-logo-height);
        }
    }

    .layout_tabbar {
        position: fixed;
        width: calc(100% - $base-menu-width);
        height: $base-tabbar-height;
        background: cyan;
        top: 0px;
        left: $base-menu-width;
    }

    .layout_main {
        position: absolute;
        width: calc(100% - $base-menu-width);
        height: calc(100vh - $base-menu-width);
        background-color: yellowgreen;
        left: $base-menu-width;
        top: $base-tabbar-height;
        padding: 20px;
        overflow: auto;
    }
}
</style>
