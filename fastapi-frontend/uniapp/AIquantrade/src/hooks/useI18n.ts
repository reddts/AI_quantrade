import { tabBarItems } from '@/config/tabbar'
import { localeMap } from '@/locale'
import { useUserStore } from '@/store'
import { computed, ref } from 'vue'

import { Locale, useCurrentLang } from 'wot-design-uni'
import enUS from 'wot-design-uni/locale/lang/en-US'
import zhCN from 'wot-design-uni/locale/lang/zh-CN'

const wotLocaleMap: Record<string, any> = {
  'zh-CN': zhCN,
  'en-US': enUS,
  //'fr-FR': frFR,
  //'ja-JP': jaJP
}

export const useI18n = () => {

  const store = useUserStore()  
  const tabbarTitles = ref({})

  // 语言包映射 默认是中文
  const getLangMap = () => {
    return localeMap[store.getLocale] || localeMap['zh-CN']
  }

  const getPagePathKey = () => {
    const pages = getCurrentPages()
    if (pages.length === 0) return ''
    const route = pages[pages.length - 1]?.route || ''
    return route.replace(/\//g, '.')
  }

  //模板翻译函数
  const t = (key: string, type?: string) => {
    const pagePathKey = getPagePathKey()
    const langMap = getLangMap()

    if (key.includes('.')) {
      // 查找全局（嵌套）字段，比如 menu.my_strategy
      const globalValue = key.split('.').reduce((obj: any, k: string) => obj?.[k], langMap)
      return type === 'text' ? computed(() => globalValue ?? '') : (globalValue ?? '')
    } else {
      // 查找当前页面路径语言字段
      const pageValue = langMap[pagePathKey]?.[key] ?? ''
      return type === 'text' ? computed(() => pageValue) : pageValue
    }
  }

  //更新 tabbar 的标题
  const updateTabbarTitles = () => {
    const langMap = getLangMap()
    tabbarTitles.value = langMap.tabbar || {}
  }

  //初始化页面标题
  const initPageTitle = () => {
    const pagePathKey = getPagePathKey()
    const langMap = getLangMap()
    const title = langMap[pagePathKey]?.NavigationTitle ?? 'unknown title'
    if (title) {
      uni.setNavigationBarTitle({ title })
    }
  }

  //改变语言并存入store
  const changeUiLang = () => {
    const currentLang = useCurrentLang().value
    const targetLang = store.getLocale
    const langPack = wotLocaleMap[targetLang]
    if (currentLang !== targetLang && langPack) {
      Locale.use(targetLang, langPack)
    }
  }

  //修改原生语言 并修改导航栏标题和tabbar
  const changeNativeLang = () => {
    initPageTitle()
    const langMap = getLangMap()
    const tabbarLocale = langMap.tabbar || {}
    const currentPage = getPagePathKey().split('.')[1] || ''
    const pagesWithoutTabbar = ['login', 'register']

    if (!pagesWithoutTabbar.includes(currentPage)) {
      tabBarItems.forEach(item => {
        const text = tabbarLocale[item.key] ?? item.key
        uni.setTabBarItem({
          index: item.index,
          text
        })
      })
    }
  }

  const setLocale = () => {
    //store.setLocale(store.getLocale)
    updateTabbarTitles()
    changeNativeLang()
    changeUiLang()
  }

 
  // 初始化语言（等页面 ready 后执行）
  // 不推荐直接在这里调用 changeNativeLang / changeUiLang
  updateTabbarTitles()

  return {
    t,
    setLocale,
    changeNativeLang,
    changeUiLang,
    updateTabbarTitles,
    tabbarTitles,
    initPageTitle
  }
}
