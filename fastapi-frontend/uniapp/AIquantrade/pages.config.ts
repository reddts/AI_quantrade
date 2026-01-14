import { defineUniPages } from '@uni-helper/vite-plugin-uni-pages'

export default defineUniPages({
  // 你也可以定义 pages 字段，它具有最高的优先级。
  pages: [],
  tabBar: {
    color: '#999',
    selectedColor: '#8fc97f',
    backgroundColor: '#fff',
    list: [
      {
        pagePath: 'pages/index/index',
        iconPath: 'static/tabbar/home.png',
        selectedIconPath: 'static/tabbar/home-active.png',
        text: 'home' // 作为 key 占位
      },
      {
        pagePath: 'pages/market/index',
        iconPath: 'static/tabbar/market.png',
        selectedIconPath: 'static/tabbar/market-active.png',
        text: 'market'
      },
      {
        pagePath: 'pages/stock/index',
        iconPath: 'static/tabbar/discover.png',
        selectedIconPath: 'static/tabbar/discover-active.png',
        text: 'stock'
      },
      {
        pagePath: 'pages/strategy/index',
        iconPath: 'static/tabbar/mine.png',
        selectedIconPath: 'static/tabbar/mine-active.png',
        text: 'strategy'
      },
      {
        pagePath: 'pages/user/index',
        iconPath: 'static/tabbar/mine.png',
        selectedIconPath: 'static/tabbar/mine-active.png',
        text: 'user'
      }
    ]
  },
  globalStyle: {
    navigationBarBackgroundColor: '#ffffff',
    navigationBarTextStyle: 'black',
    navigationBarTitleText: 'index'
  },
  easycom: {
    autoscan: true,
    custom: {
      '^wd-(.*)': 'wot-design-uni/components/wd-$1/wd-$1.vue',
      '^(?!z-paging-refresh|z-paging-load-more)z-paging(.*)': 'z-paging/components/z-paging$1/z-paging$1.vue'
    }
  }
})
