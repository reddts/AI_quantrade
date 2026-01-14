<route type="page" lang="json5">
{
  style: {
    navigationStyle: 'custom'
  }
}
</route>
<template>
    <view class="forget-password-container">
        <view class="content-wrapper">
            <view class="title">{{ t('resetPassword') }}</view>
            
            <view class="form-wrapper">
                <view class="input-item">
                    <text class="iconfont icon-phone"></text>
                    <input 
                        type="number" 
                        v-model="form.phone" 
                        :maxlength="11" 
                        :placeholder="t('phonePlaceholder')"  
                        placeholder-class="placeholder"
                    />
                </view>
                
                <view class="input-item code-item">
                    <text class="iconfont icon-safe"></text>
                    <input 
                        type="number" 
                        v-model="form.verifyCode" 
                        :maxlength="6" 
                        :placeholder="t('smsCodePlaceholder')"
                        placeholder-class="placeholder"
                    />
                    <text 
                        class="code-btn" 
                        :class="{ disabled: counting }"
                        @tap="getVerifyCode"
                    >{{ counting ? `${counter}s` : t('getCode') }}</text>
                </view>
                
                <view class="input-item">
                    <text class="iconfont icon-lock"></text>
                    <input 
                        type="safe-password" 
                        v-model="form.newPassword" 
                        :placeholder="t('newPasswordPlaceholder')" 
                        placeholder-class="placeholder"
                    />
                </view>
                
                <view class="input-item">
                    <text class="iconfont icon-lock"></text>
                    <input 
                        type="safe-password" 
                        v-model="form.confirmPassword" 
                        :placeholder="t('confirmNewPasswordPlaceholder')" 
                        placeholder-class="placeholder"
                    />
                </view>
            </view>
            
            <button class="submit-btn" @tap="handleSubmit">{{ t('confirmReset') }}</button>
        </view>
        <!--返回登陆-->
        <view class="switch-box">
            <text class="switch-btn" @tap="switchLoginType">{{  t('backToLogin') }}</text>
        </view>
    </view>
</template>

<script  setup lang="ts">
import { inject } from 'vue';
const t = inject('t') as (key: string) => string;
if (!t) {
    throw new Error("Localization function 't' is not provided. Ensure it is injected properly.");
}

const form = reactive({
    phone: '',
    verifyCode: '',
    newPassword: '',
    confirmPassword: ''
});

const counting = ref(false);
const counter = ref(60);

const getVerifyCode = () => {
    if (counting.value) return;

    if (!form.phone) {
        uni.showToast({
            title: t('enterPhoneNumber'),
            icon: 'none'
        });
        return;
    }

    if (!/^1[3-9]\d{9}$/.test(form.phone)) {
        uni.showToast({
            title: t('invalidPhoneNumber'),
            icon: 'none'
        });
        return;
    }

    counting.value = true;
    counter.value = 60;
    const timer = setInterval(() => {
        counter.value--;
        if (counter.value <= 0) {
            clearInterval(timer);
            counting.value = false;
        }
    }, 1000);

    uni.showToast({
        title: t('verificationCodeSent'),
        icon: 'success'
    });
};

const handleSubmit = () => {
    if (!form.phone || !form.verifyCode || 
        !form.newPassword || !form.confirmPassword) {
        uni.showToast({
            title: t('fillAllFields'),
            icon: 'none'
        });
        return;
    }

    if (form.newPassword !== form.confirmPassword) {
        uni.showToast({
            title: t('passwordMismatch'),
            icon: 'none'
        });
        return;
    }

    uni.showToast({
        title: t('passwordResetSuccess'),
        icon: 'success',
        duration: 2000,
        success: () => {
            setTimeout(() => {
                uni.navigateBack();
            }, 2000);
        }
    });
};

const switchLoginType = () => {
    uni.navigateTo({
        url: '/pages/login/index'
    });
};

// 设置页面标题
onMounted(() => {
  uni.setNavigationBarTitle({
    title: t('NavigationTitle') // Use the injected 't' function for localization
  });
});
</script>

<style lang="scss" scoped>
.forget-password-container {
    min-height: 100vh;
    background: #f8f9fd;
    padding: 40rpx;
}

.content-wrapper {
    margin-top: 60rpx;
}

.title {
    font-size: 40rpx;
    font-weight: 600;
    color: #333;
    margin-bottom: 60rpx;
}

.form-wrapper {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 30rpx;
    padding: 40rpx;
    box-shadow: 0 20rpx 40rpx rgba(0, 0, 0, 0.05);
    
    .input-item {
        display: flex;
        align-items: center;
        height: 100rpx;
        background: #f8f9fd;
        border-radius: 20rpx;
        padding: 0 30rpx;
        margin-bottom: 30rpx;
        
        .iconfont {
            font-size: 36rpx;
            color: #a18cd1;
            margin-right: 20rpx;
        }
        
        input {
            flex: 1;
            font-size: 28rpx;
            color: #333;
        }
        
        .placeholder {
            color: #999;
        }
    }
    
    .code-item {
        padding-right: 200rpx;
        position: relative;
        
        .code-btn {
            position: absolute;
            right: 30rpx;
            top: 50%;
            transform: translateY(-50%);
            font-size: 26rpx;
            color: #a18cd1;
            
            &.disabled {
                color: #999;
            }
        }
    }
}

.switch-box {
    margin-top: 40rpx;

    .switch-tip {
        font-size: 26rpx;
        color: #666;
    }
    
    .switch-btn {
        font-size: 26rpx;
        color: #377bf0;
        margin-left: 10rpx;
    }
 }

.submit-btn {
    width: 100%;
    height: 90rpx;
    line-height: 90rpx;
    background: linear-gradient(45deg, #a18cd1 0%, #fbc2eb 100%);
    border-radius: 45rpx;
    color: #fff;
    font-size: 32rpx;
    font-weight: 500;
    letter-spacing: 4rpx;
    margin-top: 60rpx;
    border: none;
    
    &:active {
        transform: scale(0.98);
    }
}
</style> 