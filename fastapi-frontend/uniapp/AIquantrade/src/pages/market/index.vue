<route type="tab" lang="json5">
{
  layout: 'theme', // 使用主题
  style: { 
    "navigationBarTitleText": "市场" 
   }
}
</route>
<template>
  <view class="container">
    <view class="nav">
      <wd-navbar title="首页" left-text="返回" right-text="设置" left-arrow>
        <template #capsule>
          <wd-navbar-capsule @back="handleBack" @back-home="handleBackHome" />
        </template>
      </wd-navbar>
    </view>
    <view class="content">
      <text>市场页面</text>
    </view>
  <view>
    <button @click="getTest">GET 请求</button>
    <button @click="postTest">POST 请求</button>
    <button @click="cancelRequest">取消 请求</button>
    <button @click="awaitToJs">awaitToJs</button>
  </view>
  <NavBar />
  </view>
</template>

<script setup lang="ts">
import { awaitToJsTestApi, getTestApi, postTestApi } from '@/api/testApi'
//底部导航栏
import NavBar from '@/components/nav-bar.vue'

function handleBack() {
  uni.navigateBack({})
}

function handleBackHome() {
  uni.reLaunch({ url: '/pages/index/index' })
}


// GET 请求
const getTest = async () => {
  const res = await getTestApi({ name: 'uni-lin' })
  console.log(res)
}

// POST 请求
let requestTask = null
const postTest = () => {
  requestTask = postTestApi({ name: 'uni-lin' }, { id: '123456' })
  requestTask
    .then(res => {
      console.log(res)
    })
    .catch(err => {
      console.log(err)
    })
}

// 取消 请求
const cancelRequest = () => {
  // 取消请求
  requestTask.abort()
}

/* await-to-js 代替 try catch 用法，根据实际需求进行使用 */
const awaitToJs = async () => {
  const [data, err] = await awaitToJsTestApi({ name: 'uni-lin' })
  if (data) {
    console.log(data)
  }
  if (err) {
    console.log(err)
  }
}
</script>
