// utils/userMenuConfig.ts

export const getUserMenuGroups = (t: (key: string) => string) => [
  [
    { id: 1, name: t('menu.my_strategy'), icon: '/static/ustrategy.svg', arrow: true, type: 'navigate', url: '/pages/user/strategy' },
    { id: 2, name: t('menu.my_stock'), icon: '/static/uostocks.svg', arrow: true, type: 'navigate', url: '/pages/user/stock' },
    { id: 3, name: t('menu.my_follow'), icon: '/static/ufocuson.svg', arrow: true, type: 'navigate', url: '/pages/user/follow' },
    { id: 4, name: t('menu.my_fav'), icon: '/static/ufavours.svg', arrow: true, type: 'navigate', url: '/pages/user/favriate' }
  ],
  [
    { id: 5, name: t('menu.contact'), icon: '/static/ucustomer_service.svg', arrow: true, type: 'tel', data: '12345678900' },
    { id: 6, name: t('menu.share'), icon: '/static/ushare.svg', arrow: false, type: 'share' },
    { id: 7, name: t('menu.language'), icon: '/static/ulanguage.svg', arrow: true, type: 'language' },
    { id: 8, name: t('menu.logout'), icon: '/static/ulogout.svg', arrow: false, type: 'logout' }
  ]
];
