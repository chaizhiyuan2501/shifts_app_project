<template>
    <div class="register">
        <h1>registerです</h1>
    </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router"
import { ElNotification } from "element-plus";
import useUserStore from "@/store/modules/user"

let useStore = useUserStore();
let $router = useRouter();
let register = ref();

let registerForm = reactive({
    email: "",
    name: "",
    password: "",
})

const register = async()=>{
    
}
</script>
<style scoped></style>
