import { createApp } from 'vue'
import App from '@/App.vue'
import ElementPlus from "element-plus"
import "element-plus/dist/index.css"
import router from './router'
import pinia from './store'
import "@/styles/global.scss"

import ja from 'element-plus/es/locale/lang/ja'
const app = createApp(App);

app.use(ElementPlus, {
    locale: ja
})

// import  GlobalComponent  from '@/components'

// app.use(GlobalComponent)
app.use(router);

app.use(pinia);

app.mount("#app");
