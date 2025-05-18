import { createApp } from 'vue'
import App from '@/App.vue'
import ElementPlus from "element-plus"
import "element-plus/dist/index.css"
import router from './router'

// import ja from "element-plus/dist/locale/ja.min.mjs.map"
const app = createApp(App);

// app.use(ElementPlus,{
//     locale:ja
// })

// import  GlobalComponent  from '@/components'

// app.use(GlobalComponent)
app.use(router);

app.mount("#app");
