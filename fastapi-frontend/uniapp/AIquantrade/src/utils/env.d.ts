/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_CLIENT_KEY: string
  readonly VITE_SERVER_API_BASEURL: string
  readonly VITE_SERVER_STATIC_BASEURL: string

  // 你也可以在这里添加其他 env 变量
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
