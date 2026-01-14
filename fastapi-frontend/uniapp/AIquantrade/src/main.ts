import 'uno.css'
import { createSSRApp } from 'vue'
import App from './App.vue'
import { requestInterceptor, routerInterceptor } from './interceptors'
import store from './store'
import { checkBtnPermission } from './utils'

export function createApp() {
  const app = createSSRApp(App)  

  app.config.globalProperties.$perms = checkBtnPermission

  app.use(requestInterceptor)
  app.use(routerInterceptor)
  app.use(store)
  
  // 初始化国际化
  const { t, setLocale,initPageTitle } = useI18n()
  app.config.globalProperties.$t = t
  app.config.globalProperties.$setLocale = setLocale
  app.config.globalProperties.$initPageTitle = initPageTitle
    // 提供 t 给模板使用
  app.provide('t', t)
  // 提供 setLocale 和 initPageTitle 给模板使用
  app.provide('setLocale', setLocale)
  app.provide('initPageTitle', initPageTitle)
  return {
    app
  }
}
