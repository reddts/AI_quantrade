<template>
  <view class="mask" @touchmove.stop.prevent @click.self="close">
    <view class="cropper-modal">
      <canvas
        canvas-id="cropperCanvas"
        id="cropperCanvas"
        class="canvas"
        ref="canvas"
        :style="{ width: options.cropWidth + 'px', height: options.cropHeight + 'px' }"
        @touchstart="onTouchStart"
        @touchmove="onTouchMove"
      />
      <view class="controls">
        <button class="cancel-btn" @click="close">取消</button>
        <button @click="onZoom(1.1)">放大</button>
        <button @click="onZoom(0.9)">缩小</button>
        <button @click="onSubmit">裁剪并上传</button>
      </view>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { uploadAvatar } from '@/api/userApi';
import { useUserStore } from '@/store';
import { onMounted, ref, watch } from 'vue';
import type { CropOptions } from './types';


const props = defineProps<{
  imagePath: string
  options: CropOptions
}>()

const emit = defineEmits(['success', 'close'])

//用户存储信息
const userStore = useUserStore();
//客户端连接密钥
const CLIENT_SECRET = import.meta.env.VITE_APP_CLIENT_KEY || 'default-secret'

const scale = ref(1)
const offsetX = ref(0)
const offsetY = ref(0)
const startX = ref(0)
const startY = ref(0)
const ctx = uni.createCanvasContext('cropperCanvas')

// Mock implementation of getToken function
const getToken = () => {
  return userStore.userInfo.accessToken; // Replace with actual token retrieval logic
};

const drawImage = () => {
  const { cropWidth, cropHeight } = props.options
  ctx.clearRect(0, 0, cropWidth, cropHeight)
  ctx.save()
  ctx.translate(offsetX.value, offsetY.value)
  ctx.scale(scale.value, scale.value)
  ctx.drawImage(props.imagePath, 0, 0, cropWidth, cropHeight)
  ctx.restore()
  ctx.draw()
}

const onTouchStart = (e: any) => {
  e.stopPropagation()
  e.preventDefault()
  const touch = e.touches[0]
  startX.value = touch.clientX
  startY.value = touch.clientY
}

const onTouchMove = (e: any) => {
  e.stopPropagation()
  e.preventDefault()
  const touch = e.touches[0]
  const deltaX = touch.clientX - startX.value
  const deltaY = touch.clientY - startY.value
  offsetX.value += deltaX
  offsetY.value += deltaY
  startX.value = touch.clientX
  startY.value = touch.clientY
  drawImage()
}

const onZoom = (factor: number) => {
  scale.value *= factor
  drawImage()
}

const onSubmit = () => {
  const { cropWidth, cropHeight } = props.options
  uni.canvasToTempFilePath(
    {
      canvasId: 'cropperCanvas',
      width: cropWidth,
      height: cropHeight,
      success: async res => {
        const tempFilePath = res.tempFilePath

        // #ifdef H5
        // H5 平台直接用 fetch 方式转为 blob，再构造 File 上传
        const response = await fetch(tempFilePath)
        const blob = await response.blob()
        const file = new File([blob], 'avatar.png', { type: blob.type })

        try {
            const response = await uploadAvatar(file)
            if (response.code==200) {                
              console.log("头像上传成功")
              emit('success', response.imgUrl)
            }else{
              console.log(response.msg)
            }
        } catch (e: any) {
            console.log("头像上传失败")
        }
        // #endif

        // #ifdef MP-WEIXIN || APP
        // 小程序或 App 平台直接传路径
        try {
          const uploadRes = await uni.uploadFile({
            url: '/profile/avatar',
            filePath: tempFilePath,
            name: 'avatarfile',
            header: {
              Authorization: 'Bearer ' + getToken(), // 如果有 token
              'X-Client-Secret': CLIENT_SECRET
            },
          })
          const resData = JSON.parse(uploadRes.data)
          if (resData.code === 200) {
            console.log("头像上传成功")
            emit('success', resData.data.imgUrl)
          } else {
            console.log("头像上传失败")
          }
        } catch (e) {
          console.log("上传失败")
        }
        // #endif
      },
      fail: err => {
        console.error('裁剪失败', err)
        //uni.showToast({ title: '裁剪失败', icon: 'error' })
      },
    },
    undefined
  )
}



const close = () => {
  emit('close')
}

function dataURLtoFile(dataurl: string, filename: string): File {
  const arr = dataurl.split(',')
  const mime = arr[0].match(/:(.*?);/)?.[1] || 'image/png'
  const bstr = atob(arr[1])
  let n = bstr.length
  const u8arr = new Uint8Array(n)
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n)
  }
  return new File([u8arr], filename, { type: mime })
}

onMounted(drawImage)
watch(() => props.imagePath, drawImage)
</script>

<style scoped>
.mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}
.cropper-modal {
  background: #fff;
  padding: 20rpx;
  border-radius: 16rpx;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}
.canvas {
  display: block;
  margin: 0 auto;
  border: 1px solid #ccc;
}
.controls {
  display: flex;
  justify-content: space-around;
  margin-top: 20rpx;
}
button.cancel-btn {
  background-color: #eee;
  color: #666;
}
</style>
