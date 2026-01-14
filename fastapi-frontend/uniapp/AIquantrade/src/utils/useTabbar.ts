// src/composables/useTabbar.ts
import { tabbarConfig } from '@/config/tabbar'
import { useI18n } from '@/hooks/useI18n'
import { useUserStore } from '@/store'
import { onShow as uniOnShow } from '@dcloudio/uni-app'
import { computed, ref, watch } from 'vue'

// 跳转锁，防止重复跳转
let isSwitching = false

export function useTabbar() {
  const i18n = useI18n()
  const userStore = useUserStore()
  const tabbarIndex = ref(0)

  // 国际化 tabbar 标题
  const tabbarTitles = computed(() => {
    const titlesMap = i18n.tabbarTitles.value || {}
    return tabbarConfig.map(item => ({
      ...item,
      title: titlesMap[item.key] || item.key
    }))
  })

  // 所有页面路径数组
  const pages = computed(() => tabbarConfig.map(item => item.url))

  // 页面展示时自动匹配当前路由设置高亮
  uniOnShow(() => {
    const current = getCurrentPages().slice(-1)[0]?.route || ''
    const matchedIndex = pages.value.findIndex(p => current.includes(p))
    if (matchedIndex !== -1) {
      tabbarIndex.value = matchedIndex
    } else {
      console.warn('tabbar onShow 未匹配到路径:', current)
    }
  })

  // 切换 tabbar 方法
  function onNavChange(event: any) {
    const index = event?.value ?? event // 兼容可能是对象的情况（wd-tabbar 会传对象）
    const currentRoute = getCurrentPages().slice(-1)[0]?.route || ''
    const target = pages.value[index]

    if (!target || target === currentRoute || isSwitching) return

    isSwitching = true
    tabbarIndex.value = index
    uni.switchTab({
      url: '/' + target,
      complete: () => {
        setTimeout(() => {
          isSwitching = false
        }, 500)
      }
    })
  }

  // 响应语言变化，更新 tabbar 显示文字
  watch(() => userStore.userInfo.locale, () => {
    i18n.updateTabbarTitles()
  })

  return {
    tabbarIndex,
    tabbarTitles,
    onNavChange
  }
}
