<template>
    <div class="layout_container">
        <!-- 左側サイドメニュー -->
        <div class="layout_slider">左側サイドメニュー</div>
        <!-- トップナビゲーションバー -->
        <div class="layout_tabbar">トップナビゲーション</div>
        <!-- コンテンツ表示エリア -->
        <div class="layout_main">コンテンツ表示エリア</div>
    </div>
</template>
<script setup lang="ts">

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
