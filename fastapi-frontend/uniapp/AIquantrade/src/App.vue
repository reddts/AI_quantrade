<script setup lang="ts">
import { useUserStore } from '@/store/user';
import { onHide, onLaunch, onShow } from '@dcloudio/uni-app';

//避免touchmove事件阻塞页面滚动
const originalAddEventListener = EventTarget.prototype.addEventListener;
EventTarget.prototype.addEventListener = function (
  type: string,
  listener: EventListenerOrEventListenerObject,
  options?: boolean | AddEventListenerOptions
) {
  if (type === 'touchmove' || type === 'wheel' || type === 'touchstart') {
    if (typeof options === 'object') {
      options.passive = true;
    } else {
      options = { passive: true };
    }
  }
  originalAddEventListener.call(this, type, listener, options);
};


// 获取 Pinia 实例
const userStore = useUserStore()
// 允许页面白名单（登录页、忘记密码页）
const whiteList = ['pages/login/index','pages/login/forget-password']

// 路由跳转时判断
function checkLoginStatus() {
  const currentPage = getCurrentPages().slice(-1)[0]
  const currentRoute = currentPage?.route || ''

  if (!userStore.isLogined && !whiteList.includes(currentRoute)) {
    console.warn('未登录，跳转到登录页')
    uni.redirectTo({
      url: '/pages/login/index'
    })
  }
}

onLaunch(() => {
  console.log('App Launch')
  checkLoginStatus() //全局登陆校验
})
onShow(() => {
  console.log('App Show')
})
onHide(() => {
  console.log('App Hide')
})
</script>
<style>
/* 全局页面容器类名，所有页面内容建议包一层 view.page */
.container {
  padding-bottom: 60px; /* 与 TabBar 高度保持一致 */
  box-sizing: border-box;
}
</style>