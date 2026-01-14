// src/config/tabbar.ts
export interface TabbarItem {
  key: string
  icon: string
  url: string
}

export const tabbarConfig: TabbarItem[] = [
  { key: 'home', icon: 'home', url: 'pages/index/index' },
  { key: 'market', icon: 'view', url: 'pages/market/index' },
  { key: 'stock', icon: 'heart', url: 'pages/stock/index' },
  { key: 'strategy', icon: 'chart', url: 'pages/strategy/index' },
  { key: 'user', icon: 'chat', url: 'pages/user/index' }
]

// 额外导出用于多语言设置tabbar标题的数组（index 和 key）
export const tabBarItems = tabbarConfig.map((item, index) => ({
  index,
  key: item.key
}))

export const pagesWithoutTabbar = ['login', 'register']
