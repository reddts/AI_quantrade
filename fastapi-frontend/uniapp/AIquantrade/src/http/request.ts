//该包未使用，留待备用
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | 'HEAD'

interface RequestOptions {
  method?: HttpMethod
  url: string
  data?: Record<string, any>
  params?: Record<string, any>
  headers?: Record<string, string>
  contentType?: 'json' | 'form' // 默认 json
  debounceTimeMs?: number
}

type GetTokenFunc = () => string | null

const CLIENT_SECRET = import.meta.env.VITE_APP_CLIENT_KEY || 'default-secret'

function generateRequestKey(options: RequestOptions) {
  const { method = 'GET', url, data, params } = options
  let key = method.toUpperCase() + ':' + url
  if (params && Object.keys(params).length > 0) {
    key += '?'
    key += Object.entries(params)
      .sort()
      .map(([k, v]) => `${k}=${v}`)
      .join('&')
  }
  if (data && Object.keys(data).length > 0) {
    key += '#'
    key += JSON.stringify(data)
  }
  return key
}

export class HttpService {
  private pendingRequests = new Map<string, Promise<any>>()
  private lastRequestTime = new Map<string, number>()

  constructor(private getToken?: GetTokenFunc) {}

  public async request<T = any>(options: RequestOptions): Promise<T> {
    const {
      method = 'GET',
      url,
      data,
      params,
      headers = {},
      contentType = 'json',
      debounceTimeMs = 300,
    } = options

    const requestKey = generateRequestKey(options)
    const now = Date.now()

    // 防抖
    const lastTime = this.lastRequestTime.get(requestKey)
    if (lastTime && now - lastTime < debounceTimeMs) {
      return Promise.reject(new Error('请求过于频繁，请稍后再试'))
    }
    this.lastRequestTime.set(requestKey, now)

    // 防重复请求
    if (this.pendingRequests.has(requestKey)) {
      return this.pendingRequests.get(requestKey)!
    }

    // URL 参数拼接
    let finalUrl = url
    if (params && Object.keys(params).length > 0) {
      const queryString = new URLSearchParams()
      for (const [key, value] of Object.entries(params)) {
        if (value !== undefined && value !== null) {
          queryString.append(key, String(value))
        }
      }
      finalUrl += (url.includes('?') ? '&' : '?') + queryString.toString()
    }

    // Headers 组合
    const token = this.getToken?.()
    const finalHeaders: Record<string, string> = {
      'X-Client-Secret': CLIENT_SECRET,
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    }

    // 请求体处理
    let body: string | undefined = undefined
    if (method !== 'GET' && method !== 'HEAD' && data) {
      if (contentType === 'json') {
        finalHeaders['Content-Type'] = 'application/json'
        body = JSON.stringify(data)
      } else if (contentType === 'form') {
        finalHeaders['Content-Type'] = 'application/x-www-form-urlencoded'
        body = new URLSearchParams(data as any).toString()
      } else {
        return Promise.reject(new Error(`不支持的 contentType: ${contentType}`))
      }
    }

    const fetchPromise = fetch(finalUrl, {
      method,
      headers: finalHeaders,
      body,
    })
      .then(async (res) => {
        if (!res.ok) {
          const errorText = await res.text()
          throw new Error(`HTTP ${res.status}: ${errorText}`)
        }
        try {
          return (await res.json()) as T
        } catch {
          return (await res.text()) as unknown as T
        }
      })
      .finally(() => {
        this.pendingRequests.delete(requestKey)
      })

    this.pendingRequests.set(requestKey, fetchPromise)

    return fetchPromise
  }

  public get<T = any>(url: string, options?: Omit<RequestOptions, 'method' | 'url'>) {
    return this.request<T>({ ...options, method: 'GET', url })
  }

  public post<T = any>(url: string, options?: Omit<RequestOptions, 'method' | 'url'>) {
    return this.request<T>({ ...options, method: 'POST', url })
  }

  public put<T = any>(url: string, options?: Omit<RequestOptions, 'method' | 'url'>) {
    return this.request<T>({ ...options, method: 'PUT', url })
  }

  public delete<T = any>(url: string, options?: Omit<RequestOptions, 'method' | 'url'>) {
    return this.request<T>({ ...options, method: 'DELETE', url })
  }

  public patch<T = any>(url: string, options?: Omit<RequestOptions, 'method' | 'url'>) {
    return this.request<T>({ ...options, method: 'PATCH', url })
  }
}
