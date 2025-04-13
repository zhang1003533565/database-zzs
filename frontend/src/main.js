import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router' // ✅ 引入上面定义的 router


const app = createApp(App)
app.use(router)              // ✅ 记得使用 router
app.use(ElementPlus)
app.mount('#app')
