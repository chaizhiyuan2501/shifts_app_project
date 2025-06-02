<template>
  <div class="">
    <h1>动态生成菜单根据项目路由生成</h1>
    <h1>{{ menuList }}</h1>
    <template v-for="(item,index) in menuList" :key="item.path">
        

    </template>
  </div>
</template>
<script setup lang="ts">
defineProps(["menuList"])
</script>
<style scoped>

</style>
