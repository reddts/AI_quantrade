<!-- default.vue -->
<template>
  <WdConfigProvider :theme="theme" :theme-vars="themeVars">
    <div class="">
      <slot></slot>
    </div>
  </WdConfigProvider>
</template>

<script setup lang="ts">
import { useTheme } from '@/hooks/useTheme';
const { theme, themeVars } = useTheme()
</script>

<style>
/* 默认主题 */
:root page {
  color: #000000;
  background: #f5f5f5;
  --theme-bg-color: #ffffff;
}
</style>
