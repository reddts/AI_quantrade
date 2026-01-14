// utils/upload.ts
import { useUserStore } from '@/store'

export interface UploadParams {
  url: string
  filePath: string
  name?: string
  data?: Record<string, any>
  header?: Record<string, string>
}

export function uploadFileWithAuth(params: UploadParams): Promise<any> {
  const store = useUserStore()
  const token = store.userInfo?.accessToken
  const CLIENT_SECRET = import.meta.env.VITE_APP_CLIENT_KEY

  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: params.url.startsWith('http')
        ? params.url
        : import.meta.env.VITE_SERVER_API_BASEURL + params.url,
      filePath: params.filePath,
      name: params.name || 'file',
      formData: params.data || {},
      header: {
        'X-Client-Secret': CLIENT_SECRET,
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(params.header || {})
      },
      success(res) {
        try {
          const result = JSON.parse(res.data)
          if (result.code === 200) {
            resolve(result)
          } else {
            uni.showToast({ title: result.msg || 'Upload Failed', icon: 'none' })
            reject(result)
          }
        } catch (err) {
          reject(err)
        }
      },
      fail(err) {
        uni.showToast({ title: 'Upload Failed', icon: 'none' })
        reject(err)
      }
    })
  })
}
