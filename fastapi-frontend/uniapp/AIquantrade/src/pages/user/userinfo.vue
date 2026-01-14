<route type="page" lang="json5">
{
  layout: 'default', // 使用主题
  style: {navigationStyle: 'custom'}
}
</route>
<template>
	<view class="container">
		<view class="nav">
		<wd-navbar :title="t('NavigationTitle')" :left-text="t('common.back')" right-text="" left-arrow>
			<template #capsule>
			<wd-navbar-capsule @back="handleBack" @back-home="handleBackHome" />
			</template>
		</wd-navbar>
		</view>
		<view class="ui-all">
			<view class="avatar" @tap="showAvatarCropper = true">
				<view  class="imgAvatar">
					<view class="iavatar" :style="'background: url('+avatar+') no-repeat center/cover #eeeeee;'"></view>
				</view>
				<text v-if="avatar" @click="selectImage('avatar')">{{ t('modifyAvatar') }}</text>
				<text v-if="!avatar" @click="selectImage('avatar')">{{ t('uploadAvatar') }}</text>
				<!---<button v-if="!avatar" open-type="getUserInfo" @tap="getUserInfo" class="getInfo"></button>-->
    				<!--<button @click="selectImage('image')">上传图片</button>-->

				    <!-- 头像上传组件 -->
					<!--<avatar-upload
					v-if="showAvatarCropper"
					@close="showAvatarCropper = false"
					@success="onAvatarUpdated"
					/>-->
					<ImageCropper
						v-if="imagePath"
						:imagePath="imagePath"
						:options="cropOptions"
						@success="onCropSuccess"
						@close="onClose"
					/>
			</view>
			<form v-if="isH5Platform">
			<wd-form ref="form" :model="userform">
				<wd-cell-group  label-width="10"  border>
					<wd-input
						:label="t('username')"
						label-width="120rpx"
						prop="userform.username"
						readonly
						v-model="userform.username"
						/>
					<wd-input
						:label="t('nickname')"
						label-width="120rpx"
						prop="userform.nickname"
						clearable
						v-model="userform.nickname"
						/>
					<wd-input
						:label="t('oldpassword')"
						label-width="120rpx"
						prop="userform.oldpassword"
						show-password
						clearable
						v-model="userform.oldpassword"
						:placeholder="t('passwordPlaceholder')"
						/>
					<wd-input
						:label="t('newpassword')"
						label-width="120rpx"
						prop="userform.password"
						show-password
						clearable
						v-model="userform.password"
						:placeholder="t('passwordPlaceholder')"
						/>
					<wd-input
						:label="t('confirmPassword')"
						label-width="120rpx"
						prop="userform.confirmpassword"
						show-password
						clearable
						v-model="userform.confirmpassword"
						:placeholder="t('passwordPlaceholder')"
						/>
					<wd-input
						type="text"
						:label="t('email')"
						label-width="120rpx"
						v-model="userform.email"
						:placeholder="t('emailPlaceholder')"
						/>
                    <wd-picker
						:columns="theme"
						:label="t('theme')"
						label-width="120rpx"
						v-model="userform.theme"
						/>
					<wd-picker
						:columns="sex"
						:label="t('gender')"
						label-width="120rpx"
						v-model="userform.sex"

						/>
					<wd-input
						type="text"
						:label="t('phonenumber')"
						label-width="120rpx"
						v-model="userform.phonenumber"
						:placeholder="t('phoneNumberPlaceholder')"
						/>
					<wd-calendar v-model="userform.birthday" :label="t('birthday')" @confirm="handleConfirm" />
  					<wd-textarea
						:label="t('signature')"
						label-width="120rpx"
						:maxlength="100"
						clearable
						show-word-limit						
						auto-height
						v-model="userform.signature"
						:placeholder="t('signaturePlaceholder')"
						/>
						<wd-textarea
						:label="t('remark')"
						label-width="120rpx"
						:maxlength="100"
						clearable
						show-word-limit											
						auto-height
						v-model="userform.remark"
						:placeholder="t('signatureRemarkPlaceholder')"
						/>
				</wd-cell-group>
				

				<wd-button class="save" @tap="handleSubmit" block>{{ t('submitForm') }}</wd-button>
			</wd-form>
			</form>
		</view>

	</view>
</template>

<script lang="ts" setup>
import { getUserProfile, updateUserPassword, updateUserProfile } from '@/api/userApi'; // Adjust the import path as necessary
import { useUserStore } from '@/store';
import { reactive, ref } from 'vue';

import ImageCropper from '@/components/ImageCropper/ImageCropper.vue';
import type { CropMode, CropOptions } from '@/components/ImageCropper/types';


const t = inject('t') as (key: string) => string
const initPageTitle = inject('initPageTitle') as () => void;


const userStore = useUserStore();
const isH5Platform = process.env.VUE_APP_PLATFORM === 'h5'; // Define a constant for platform check

const userform = reactive({
	userid: userStore.userInfo.userId || '', // Ensure userId is initialized
	username: userStore.userInfo.userName || '', // Ensure userName is initialized
	nickname: userStore.userInfo.nickName || '', // Ensure nickName is initialized
	oldpassword: '', // Initialize password with an empty string
	password: '', // Initialize password with an empty string
	confirmpassword: '',
	email: userStore.userInfo.email || '', // Ensure email is initialized
	sex: userStore.userInfo.sex || '',
	birthday: userStore.userInfo.birthday ? new Date(userStore.userInfo.birthday).getTime() : new Date('1980-10-10').getTime(), // Convert to timestamp, default to 1980-10-10
	phonenumber: userStore.userInfo.phonenumber || '', // Added phonenumber property
	signature: userStore.userInfo.signature || '', // Added signature property
	remark: userStore.userInfo.remark || '', // Added remark property
	theme: userStore.userInfo.theme || 'light' // Added theme property
});

//当页面加载时
onMounted(async () => {
	initPageTitle()
	if(!userStore.userInfo) {
		// 如果 userInfo 为空，请求用户信息
		await getUserProfile().then((res) => {
			userStore.setUserInfo(res.data);
		}).catch((error) => {
			console.error('获取用户信息失败:', error);
		});
	}
});


const sex = ref([
	{ label: t('genderMale'), value: '0' },
	{ label: t('genderFemale'), value: '1' },
	{ label: t('genderNotSpecified'), value: '2' }
]);

const theme = ref(['light', 'dark']); // Define theme as a ref

const avatar = ref(userStore.userInfo.avatar || ''); // Define avatar as a ref, default to userStore's avatar
const showAvatarCropper = ref(false); // Define showAvatarCropper as a ref

//头像弹窗默认属性
const imagePath = ref('')
const cropOptions = ref<CropOptions>({
  mode: 'avatar',
  aspectRatio: 1,
  cropWidth: 128,
  cropHeight: 128,
})

//头像弹窗选择图片
const selectImage = (mode: CropMode) => {
  uni.chooseImage({
    count: 1,
    success: res => {
      imagePath.value = res.tempFilePaths[0]
      cropOptions.value =
        mode === 'avatar'
          ? { mode, aspectRatio: 1, cropWidth: 128, cropHeight: 128 }
          : { mode, aspectRatio: 4 / 3, cropWidth: 800, cropHeight: 600 }
    },
  })
}

//头像更新成功方法
const onCropSuccess = (filePath: string) => {
	avatar.value = filePath
	//更新用户头像属性
	userStore.setUserInfo({avatar:filePath})
	imagePath.value = '' // 隐藏裁剪组件
	uni.showToast({ title: t('avatarUpdateSuccess'), icon: 'success' })
}


//头像更新弹窗关闭
const onClose = () => {
  imagePath.value = ''  // 关闭裁剪弹窗
}

//日期选择框
const handleConfirm = (selectedDate) => {
	console.log('Selected Date:', selectedDate);
	userform.birthday = selectedDate.value;
};
	
//用户信息表单提交
async function handleSubmit() {
	if (!userform.nickname) {
		uni.showToast({
			title: t('nicknameRequired'),
			icon: 'none',
			duration: 2000
		});
		return;
	}
	if (userform.password) {
		//如果旧密码不填提示旧密码未填
		if (!userform.oldpassword) {
			uni.showToast({
				title: t('oldPasswordRequired'),
				icon: 'none',
				duration: 2000
			});
			return;
		}
		if( userform.password !== userform.confirmpassword){
			//如果新密码和确认密码不一致提示
			uni.showToast({
				title: t('passwordMismatch'),
				icon: 'none',
				duration: 2000
			});
			return;
		}
	}
	//验证填写的email邮箱是否正确
	if (userform.email && !/^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test(userform.email)) {
		uni.showToast({
			title: t('invalidEmail'),
			icon: 'none',
			duration: 2000
		});
		return;
	}
	//调用api提交表单

	let isSubmitting = false; // 防止重复提交标志

	if (isSubmitting) {
		uni.showToast({
			title: t('submitting'),
			icon: 'none',
			duration: 2000
		});
		return;
	}

	isSubmitting = true;

	// 防抖处理
	setTimeout(async () => {
		//如果密码字段不为空，则调用更新密码API方法
		if (userform.password && userform.password === userform.confirmpassword) {
			userform.password = userform.password.trim(); // 去除密码前后的空格
			try{
				await updateUserPassword(userform.oldpassword, userform.password);
			}catch (error) {
				console.error('更新密码失败:', error);
				uni.showToast({
					title: t('updatepasswordfaild') + ',' +error.data.msg,
					icon: 'none',
					duration: 2000
				});
				isSubmitting = false; // 重置提交状态
				return;
			}
			
		}
		try {
			await updateUserProfile(userform)
		} catch (error) {
			console.error('更新用户信息失败:', error);
			uni.showToast({
				title: t('updateinfofaild') + ',' + error.data.msg,
				icon: 'none',
				duration: 2000
			});
			isSubmitting = false; // 重置提交状态
			return;

		} finally {
			// 更新用户信息到 store
			userStore.setUserInfo({
				...userform,
				avatar: avatar.value // 更新头像
			});
			isSubmitting = false;
		}
		uni.showToast({
			title: t('updateinfosuccess'),
			icon: 'success',
			duration: 2000
		});
		
	}, 300); // 防抖时间设置为300ms

}

//导航栏按钮区
function handleBack() {
	uni.switchTab({
  		url: '/pages/user/index'  // 注意必须是 tabBar 页面中定义的 path
	})
}

function handleBackHome() {
  uni.reLaunch({ url: '/pages/index/index' })
}


</script>

<style lang="scss">
	.container {
		display: block;
	}
	.userform{
		padding: 8rpx 15rpx;

	}


	.ui-all {
		padding: 20rpx 40rpx;

		.avatar {
			width: 100%;
			text-align: left;
			padding: 20rpx 0;
			border-bottom: solid 1px #f2f2f2;
			position: relative;

			.imgAvatar {
				width: 160rpx;
				height: 160rpx;
				border-radius: 50%;
				display: inline-block;
				vertical-align: middle;
				overflow: hidden;

				.iavatar {
					width: 100%;
					height: 100%;
					display: block;
				}
			}

			text {
				display: inline-block;
				vertical-align: middle;
				color: #8e8e93;
				font-size: 28rpx;
				margin-left: 40rpx;
			}

			&:after {
				content: ' ';
				width: 20rpx;
				height: 20rpx;
				border-top: solid 1px #030303;
				border-right: solid 1px #030303;
				transform: rotate(45deg);
				-ms-transform: rotate(45deg);
				/* IE 9 */
				-moz-transform: rotate(45deg);
				/* Firefox */
				-webkit-transform: rotate(45deg);
				/* Safari 和 Chrome */
				-o-transform: rotate(45deg);
				position: absolute;
				top: 85rpx;
				right: 0;
			}
		}

		.save {			
			margin-top: 40rpx;
			font-size: 28rpx;
		}
	}
</style>
