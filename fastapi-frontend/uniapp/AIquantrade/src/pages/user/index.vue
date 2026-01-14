<route type="tab" lang="json5">
{
  layout: 'default', // 使用主题
  style: {navigationStyle: 'custom'}
}
</route>
<template>
	<view class="page">
		<view class="action">
			<view><image src="/static/uscan.svg"></image></view>
			<view><image src="/static/usetting.svg"></image></view>
		</view>
		<view class="user" @click="navigateToUserInfo">
			<!--用户基本信息-->
			<image 
				class="avatar" 
				:src="userInfo.avatar || (userInfo.sex === '0' ? '/static/avatar_m.svg' : '/static/avatar_fm.svg')">
			</image>
			<view class="name">
				<text>{{ userInfo.nickName }}</text>
				<text>{{ userInfo.remark}}</text>
			</view>
			<image class="right" src="/static/uright.svg"></image>
		</view>
		<view class="tip"> 
			<view>
				<!--选股个数-->
				<text>{{ t("myPickStock") }}</text>
				<text>13</text>
			</view>
			<view>
				<!--关注次数-->
				<text>{{ t("myFocked") }}</text>
				<text>189</text>
			</view>
			<view>
				<!--登陆次数-->
				<text>{{ t("myLogin") }}</text>
				<text>347</text>
			</view>
		</view>
		
		<view class="card" v-for="(group, index) in menuGroups" :key="index">
			<view class="menu">
				<view
					class="item"
					v-for="item in group"
					:key="item.id"
					@click="handleMenuClick(item)"
				>
					<image :src="item.icon" />
					<view>{{ item.name }}</view>
					<image class="arrow" v-if="item.arrow" src="/static/uright.svg" />
				</view>
			</view>
		</view>
		<view>
			<wd-divider dashed>{{ t('authorText') }}</wd-divider>
		</view>
		<!--语言选择器-->
		<LanguageSelector ref="langSelectorRef" />
		<NavBar />
	</view>
</template>


<script setup lang="ts">
import { logoutApi } from '@/api/loginApi';
import LanguageSelector from '@/components/language-selector.vue'; // 语言选择组件
import NavBar from '@/components/nav-bar.vue'; // 导航栏组件
import { useUserStore } from '@/store';
import { getUserMenuGroups } from '@/utils/userMenuConfig'; //加载用户中心菜单
import { inject, ref } from 'vue';


const t = inject('t') as (key: string) => string
const initPageTitle = inject('initPageTitle') as () => void;

const UserStore= useUserStore(); // 使用 Pinia 的用户状态管理
const userInfo = UserStore.userInfo; // 获取用户信息


// Navigate to user info page
const navigateToUserInfo = () => {
	uni.navigateTo({
		url: '/pages/user/userinfo'
	});
};

// 导入或定义生成分享二维码的函数
import { generateShareQRCode } from '@/utils/shareUtils'; // 假设该函数在 utils/shareUtils.ts 中

const langSelectorRef = ref()

//用户中心菜单
const menuGroups = computed(() => getUserMenuGroups(t)) // 使用 computed 确保 t 可用后再调用

// 统一处理点击事件
const handleMenuClick = (item: any) => {
	switch (item.type) {
		case 'navigate':
			uni.navigateTo({
				url: item.url
			});
			break;
		case 'tel':
			uni.makePhoneCall({
				phoneNumber: item.data
			});
			break;
		case 'share':
			const shareurl=import.meta.env.VITE_APP_SHARE_URL+ '/pages/index/index';
			if (uni.getSystemInfoSync().platform === 'mp-weixin') {
				uni.share({
					provider: 'weixin',
					type: 0,
					title: t('shareAppTitle'),
					summary: t('shareAppSummary'),
					href: shareurl,
					imageUrl: '/static/share-bg.png',
				});
			} else {
				// 调用封装的生成分享二维码函数
				generateShareQRCode(shareurl, '/static/share-bg.png');
			}
			break;
		case 'language':
			// 显示语言选择器
			if (langSelectorRef.value) {
				langSelectorRef.value.show = true;
			}
			break;
		case 'logout':
			logout();
			break;
		default:
			console.warn('未知菜单操作类型', item);
	}
}

//退出登陆功能
function logout() {
	uni.showModal({
		title: t('logoutPromptTitle'),
		content: t('logoutPromptMessage'),
		success: (res) => {
			if (res.confirm) {
				// 清除用户信息
				logoutApi().then(() => {					
					// 跳转到登录页
					uni.redirectTo({
						url: '/pages/login/index'
					});
					
				}).catch((error) => {
					console.error('退出登录失败:', error);
					uni.showToast({
						title: t('logoutFailedTitle'),
						icon: 'none'
					});
				});
			}
		}
	});
}


// 设置页面标题
onMounted(() => {
	initPageTitle()
});
</script>

<style lang="scss">
	.page {
		background: #f5f5f5;
		min-height: 100vh;
		
		.action{
			display: flex;
			justify-content: flex-end;
			padding: 10rpx;
			background: #fff;
			
			view{
				padding: 10rpx;
				margin: 0 10rpx;
				border-radius: 8rpx;
				width: 45rpx;
				height: 45rpx;
				
				&:active{
					background: #ccc;
				}
				image{
					width: 45rpx;
					height: 45rpx;
				}
			}
		}
		
		.user{
			display: flex;
			align-items: center;
			padding: 25rpx;
			background: #fff;
			
			&:active{
				background: #f0f0f0;
			}
			
			.avatar{
				width: 180rpx;
				height: 180rpx;
				padding: 0 20rpx;
				border-radius: 50%;
			}
			.right{
				width: 30rpx;
				height: 30rpx;
			}
			.name{
				flex-grow: 1;
				display: flex;
				flex-direction: column;
				padding-left: 20rpx;
				
				text{
					&:nth-child(1){
						font-size: 16px;
						font-weight: bold;
					}
					&:nth-child(2){
						font-size: 12px;
						color: #777;
					}
				}
			}
		}
		
		.tip{
			background: #4776EC;
			width: 700rpx;
			margin: auto;
			height: 100rpx;
			border-radius: 12rpx;
			margin-top: 20rpx;
			display: flex;
			justify-content: space-between;
			align-items: center;
			color: #fff;
			
			view{
				padding-left: 20rpx;
				width: 330rpx;
				
				text{
					font-size: 14px;
					&:nth-child(2){
						font-size: 16px;
						font-weight: bold;
						margin-left: 10rpx;
					}
				}
			}
		}
		
		.card {
			background: #fff;
			box-sizing: border-box;
			width: 700rpx;
			margin: auto;
			padding: 0; // 内边距取消，由 .item 控制
			margin-top: 20rpx;
			border-radius: 12rpx;
			overflow: hidden;
			box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.05);

			.menu {
				.item {
					display: flex;
					align-items: center;
					height: 100rpx;
					padding: 0 20rpx;
					box-sizing: border-box;
					position: relative;
					background-color: #fff;

					&:active {
						background: #f6f6f6;
					}

					image {
						height: 45rpx;
						width: 45rpx;
					}

					view {
						font-size: 28rpx;
						color: #444;
						padding-left: 15rpx;
						box-sizing: border-box;
						width: calc(100% - 100rpx);
					}

					.arrow {
						width: 26rpx;
						height: 26rpx;
					}

					// 下划线分隔线（除了最后一个）
					&::after {
						content: '';
						position: absolute;
						left: 20rpx;
						right: 20rpx;
						bottom: 0;
						height: 1rpx;
						background-color: #eee;
					}

					// 最后一个 item 不显示分隔线
					&:last-child::after {
						display: none;
					}
				}
			}
		}

		
	}
</style>