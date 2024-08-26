import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import 'normalize.css'
import 'ant-design-vue/dist/reset.css'
import 'vxe-table/lib/style.css'
import { message } from 'ant-design-vue'

import { registerGlobComp } from '@/components/registerGlobComp'
import ElementTiptapPlugin from 'element-tiptap-vue3-niyuta'
import '@/styles/style.css'
const app = createApp(App).use(router).use(ElementPlus).use(createPinia().use(piniaPluginPersistedstate)).use(ElementTiptapPlugin)
app.config.globalProperties.$message = message
registerGlobComp(app)
app.mount('#app')
