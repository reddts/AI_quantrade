import { getCodeImg } from '@/api/loginApi'
import { defineStore } from 'pinia'

export const useCaptchaStore = defineStore('captcha', {
  state: () => ({
    codeImgUrl: '',
    uuid: ''
  }),
  actions: {
    async fetchCaptcha() {
        await getCodeImg().then((res) => {
            if (res.code === 200) {
                this.codeImgUrl = `data:image/png;base64,${res.img}`
                this.uuid = res.uuid
            } else {
                uni.showToast({
                    title: '获取验证码失败',
                    icon: 'none'
                })
            }
        })      
    },
    clearCaptcha() {
      this.codeImgUrl = ''
      this.uuid = ''
    }
  }
})
