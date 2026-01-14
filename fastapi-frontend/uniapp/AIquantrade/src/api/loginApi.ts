import http from '@/http/httpClient';
import { useUserStore } from '@/store';
import { useCaptchaStore } from '@/store/captchaStore';

const store = useUserStore()
//图形验证码缓存
const captchaStore = useCaptchaStore()

// /* 登录 获取 accessToken */
export const loginApi = async (form) => {
 
    const formDataStr = new URLSearchParams({
      username: form.username,
      password: form.password,
      code: form.code,
      uuid: form.uuid
    }).toString()

    const res: any = await http.post('/login', {
      data: formDataStr,
      header: {
        isToken: false,
        repeatSubmit: false,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    return res
}


// 获取验证码
export const getCodeImg = async () => {
  const res: any = await http.get('/captchaImage', {
    header: {
      isToken: false
    },
    timeout: 5000
  })
  return res
}

//注册
export const registerApi = async data => {
  const res: any = await http.post('/register', {
    header: {
      isToken: false,
    },
    data: JSON.stringify(data)
  })
  return res
}

/* 拿 refreshToken 换取 accessToken 与 新 refreshToken */
/* 即刷新 accessToken */
export const refreshTokenApi = async () => {
  const store = useUserStore()
  const { refreshToken } = store.userInfo || {}
  const res: any = await http.get('/refresh_token', {
    data: {
      refreshToken: refreshToken
    },
    header: {
        isToken: false,
        repeatSubmit: false,
      }
  })
  console.log('刷新 token', res)
  store.setUserInfo({
    refreshToken: res.data.refreshToken,
    accessToken: res.data.accessToken
  })
  return res
}

/* 获取用户信息 */
export const getUserApi = async () => {
  const res: any = await http.get('/getInfo')
  return res
}


//退出登陆
export const logoutApi = async () => {
  const res: any = await http.post('/logout', {
    header: {
      isToken: true
    }
  })
  store.clearUserInfo()
 
  return res
  
}