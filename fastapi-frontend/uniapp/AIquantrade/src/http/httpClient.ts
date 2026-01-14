import { refreshTokenApi } from '@/api/loginApi'
import { CustomRequestOptions } from '@/interceptors/request'
import { useUserStore } from '@/store'
import { uploadFileWithAuth } from '@/utils/upload'

type CustomRequestOptionsOmit = Omit<CustomRequestOptions, 'url' | 'method'>

let refreshing = false
let taskQueue: (() => void)[] = []

async function handleTokenRefresh(): Promise<boolean> {
  const store = useUserStore()
  try {
    const res: any = await refreshTokenApi()
    if (res?.data?.code === 200 && res.data.data?.access_token) {
      store.setAccessToken(res.data.data.access_token)
      store.setRefreshToken(res.data.data.refresh_token)
      return true
    }
  } catch (error) {
    console.error('刷新 token 失败', error)
  }
  return false
}

function retryQueuedRequests() {
  taskQueue.forEach(callback => callback())
  taskQueue = []
}

export default class ApiClient {
  private static http<T>(options: Omit<CustomRequestOptions, 'isBaseUrl'>) {
  const store = useUserStore()
  const { accessToken: token, refreshToken } = store.userInfo || {}

  // 这里先复制一份 header，防止后续覆盖问题
  let headers: Record<string, string> = { ...(options.header || {}) }

  // 重新检测是否是 FormData
  const isFormData = typeof FormData !== 'undefined' && options.data instanceof FormData

  // 如果是 FormData，强制删除 Content-Type，避免被错误设置
  if (isFormData && headers['Content-Type']) {
    delete headers['Content-Type']
  }

  // 这里统一注入 Authorization，覆盖 interceptor 里设置也没关系，保持最新 token
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  // 赋值回 options.header，保证最终请求使用此 headers
  options.header = headers

  return new Promise<ResData<T>>((resolve, reject) => {
    const requestTask = uni.request({
      ...options,
      // 这里使用处理过的 header
      header: options.header,
      success: async (res: any) => {
        const { statusCode, data } = res

        if (statusCode >= 200 && statusCode < 300 && data?.code === 200) {
          return resolve(data as ResData<T>)
        }

        if ((statusCode === 401 || data?.code === 401) && refreshToken && !refreshing) {
          taskQueue.push(() => this.http<T>(options).then(resolve).catch(reject))

          if (!refreshing) {
            refreshing = true
            const success = await handleTokenRefresh()
            refreshing = false

            if (success) {
              retryQueuedRequests()
            } else {
              taskQueue = []
              store.clearUserInfo()
              uni.showToast({ title: 'Your login has expired, please log in again', icon: 'none', duration: 2500 })
              setTimeout(() => {
                uni.navigateTo({ url: '/pages/login/index' })
              }, 2500)
            }
          }
          return
        }

        uni.showToast({
          title: data?.msg || data?.message || 'Request failed',
          icon: 'none'
        })
        reject(res)
      },
      fail: err => {
        if (err.errMsg === 'request:fail abort') {
          console.log(`Request ${options.url} Cancelled`)
        }
        reject(err)
      }
    })

    return {
      abort: () => requestTask.abort()
    }
  })
}

  public static get(url: string, options?: CustomRequestOptionsOmit) {
    return this.http({ url, method: 'GET', ...options })
  }

  public static post(url: string, options?: CustomRequestOptionsOmit) {
    let finalOptions = options || {}

    const isFormData =
      typeof FormData !== 'undefined' && finalOptions.data instanceof FormData

    if (isFormData) {
      const formData = finalOptions.data as FormData

      const uploadFields: Record<string, string> = {}
      let fileFieldName: string | null = null
      let filePath: string | null = null

      for (const [key, value] of formData.entries()) {
        if (
          typeof value === 'object' &&
          (value instanceof File || value instanceof Blob || 'uri' in value || 'path' in value)
        ) {
          // 遇到第一个文件类型字段
          if (!fileFieldName) {
            fileFieldName = key
            filePath =
              'uri' in value
                ? (value as any).uri
                : 'path' in value
                ? (value as any).path
                : URL.createObjectURL(value) // H5 fallback
          }
        } else {
          uploadFields[key] = String(value)
        }
      }

      if (!fileFieldName || !filePath) {
        console.warn('[ApiClient.post] FormData 中未找到有效文件字段，终止上传')
        return Promise.reject('FormData Missing uploadable file field')
      }

      // ✅ 使用你的封装函数 uploadFileWithAuth
      return uploadFileWithAuth({
        url,
        filePath,
        name: fileFieldName,
        data: uploadFields,
        header: finalOptions.header
      })
    }

    // ✅ 若为 x-www-form-urlencoded
    if (
      finalOptions.header?.['Content-Type'] === 'application/x-www-form-urlencoded' &&
      typeof finalOptions.data === 'object' &&
      !(finalOptions.data instanceof FormData)
    ) {
      finalOptions = {
        ...finalOptions,
        data: Object.entries(finalOptions.data)
          .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
          .join('&')
      }
    }

    return this.http({ url, method: 'POST', ...finalOptions })
  }

  public static put(url: string, options?: CustomRequestOptionsOmit) {
    return this.http({ url, method: 'PUT', ...options })
  }

  public static delete(url: string, options?: CustomRequestOptionsOmit) {
    return this.http({ url, method: 'DELETE', ...options })
  }
}
