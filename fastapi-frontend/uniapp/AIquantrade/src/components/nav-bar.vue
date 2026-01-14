
<template>
  <view class="tabbar-container">    
  <wd-tabbar
    v-model="tabbarIndex"
    @change="onNavChange"
    active-color="#ee0a24"
    inactive-color="#7d7e80"
    fixed
    bordered
    safeAreaInsetBottom
    placeholder
  >
    <wd-tabbar-item
      v-for="(item, index) in tabbarTitles"
      :key="index"
      :title="item.title"
      :icon="item.icon"
    />
  </wd-tabbar>
  </view>
</template>

<script setup lang="ts">
import { useTabbar } from '@/utils/useTabbar';

const { tabbarIndex, tabbarTitles, onNavChange } = useTabbar()
</script>

<style scoped>
.tabbar-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 999;
  background-color: #fff;
}
</style>
