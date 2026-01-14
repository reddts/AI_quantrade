import { useUserStore } from '@/store'
import { qs } from '@/utils'

export type HttpMethod =
  | 'GET'
  | 'POST'
  | 'PUT'
  | 'DELETE'
  | 'OPTIONS'
  | 'HEAD'
  | 'TRACE'
  | 'CONNECT'
  | 'PATCH'

export type CustomRequestOptions = UniApp.RequestOptions & {
  query?: Record<string, any>
  /** 出错时是否隐藏错误提示 */
  hideErrorToast?: boolean
  /** 自定义 content-type 类型：json | form */
  contentType?: 'json' | 'form'
  method?: HttpMethod
}

const timeout = 30000 // 请求超时时间
const baseUrl = import.meta.env.VITE_SERVER_API_BASEURL as string // 请求基础路径
const CLIENT_SECRET = import.meta.env.VITE_APP_CLIENT_KEY // 自定义头部（如需要）

// 拦截器配置
const httpInterceptor = {
  // 请求前的拦截
  invoke(options: CustomRequestOptions) {
    // 1. 设置请求路径
    if (!options.url.includes('//')) {
      // 非完整路径，补全基础路径
      // 完整路径：http://localhost:8080/api/user/login
      // 非完整路径：api/user/loginApi
      options.url = baseUrl + options.url
    }
    // 2. query 参数处理
    if (options.query) {
      // qs.stringify() 方法将一个 JavaScript 对象或数组转换为一个查询字符串
      // 比如： { name: 'tom', age: 18 } 转换成 name=tom&age=18
      const query = qs.stringify(options.query)
      options.url += options.url.includes('?') ? '&' : '?' + query
    }
    // 3. 请求超时时间设置
    options.timeout = timeout
    // 4. 定义请求返回数据的格式（设为 json，会尝试对返回的数据做一次 JSON.parse）
    options.dataType = 'json'
    // #ifndef MP-WEIXIN
    options.responseType = 'json'
    // #endif
    // 5. 添加请求头标识，可以告诉后台是小程序端发起的请求
    let resolvedContentType = 'application/json; charset=utf-8'
    if (options.contentType === 'form') {
      resolvedContentType = 'application/x-www-form-urlencoded'
      // 自动将 data 转换为 urlencoded 格式（仅限 POST/PUT）
      if (
        options.method === 'POST' ||
        options.method === 'PUT'
      ) {
        if (options.data && typeof options.data === 'object') {
          options.data = qs.stringify(options.data)
        }
      }
    }

    // 6. 合并请求头：保留调用者自定义的 header，优先使用外部传入的 Content-Type
    options.header = {
      'Content-Type': options.header?.['Content-Type'] || resolvedContentType,
      'X-Client-Secret': CLIENT_SECRET,
      ...(options.header || {})
    }

    // 7. 注入 token
    const store = useUserStore()
    const { accessToken } = store.userInfo || {}
    if (accessToken) {
      options.header.Authorization = `Bearer ${accessToken}`
    }

    return options
  }
}

export const requestInterceptor = {
  install() {
    // 拦截 request 请求
    uni.addInterceptor('request', httpInterceptor)
  }
}
