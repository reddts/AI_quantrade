<template>
  <wd-action-sheet
    v-model="show"
    :actions="computedActions"
    @close="show = false"
    @select="onSelect"
  />
</template>

<script setup lang="ts">
import { useUserStore } from '@/store'
import { computed, ref } from 'vue'
const setLocale = inject('setLocale') as () => void

const show = ref(false)
const userStore = useUserStore()
const currentLng = [
  { label: '当前语言', value: 'zh-CN' },
  { label: 'Current language', value: 'en-US' },
]

const languages = [
  { label: '简体中文', value: 'zh-CN' },
  { label: 'English', value: 'en-US' },
  //  { label: '繁體中文', value: 'zh-TW' },
  //{ label: '日本語', value: 'ja-JP' },
 // { label: '한국어', value: 'ko-KR' },
  //{ label: 'Français', value: 'fr-FR' },
  //{ label: 'Deutsch', value: 'de-DE' },
  //{ label: 'Español', value: 'es-ES' },
  //{ label: 'Русский', value: 'ru-RU' }
]

// 当前语言名
const currentLabel = computed(() =>
  languages.find(l => l.value === userStore.getLocale)?.label ?? 'unknowLanguage'
)

const currentNLabel = computed(() =>
  currentLng.find(l => l.value === userStore.getLocale)?.label ?? 'unknowLanguage'
)

// 第一项为当前语言提示（不可选）
const computedActions = computed(() => [

  {
    name: currentNLabel.value + `：${currentLabel.value}`,
    value: '__current__',
    disabled: true
  },
  ...languages
    .filter(l => l.value !== userStore.getLocale)
    .map(l => ({
      name: l.label,
      value: l.value
    }))
])

// 切换语言处理
async function onSelect({ item, index }) {
  console.log('选择的语言:', item.value)
  if ( item.value && typeof item === 'object' && 'value' in item && item.value !== '__current__') {
    try {
      // 设置用户选择的语言
      await userStore.setLocale(item.value)
      console.log('语言切换成功:', item.value)
      //切换语言
      await setLocale()
    } catch (err) {
      console.error('语言切换失败:', err)
    }
  }
  show.value = false
}

// 提供外部调用方法
defineExpose({ show })
</script>
