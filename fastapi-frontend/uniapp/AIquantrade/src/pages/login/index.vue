<route type="page" lang="json5">
{
  style: {
    navigationStyle: 'custom',
  }
}
</route>
<template>
    <view class="login-container">
        <!-- 背景动画层 -->
        <view class="bg-animation">
            <view class="circle circle-1"></view>
            <view class="circle circle-2"></view>
            <view class="circle circle-3"></view>
        </view>
        
        <!-- 主内容区 -->
        <view class="content-wrapper">
            <!-- Logo区域 -->
            <view class="logo-box">
                <text class="logo-text">{{ isLogin ? 'Welcome Back' : 'Join Us' }}</text>
                <text class="sub-title">{{ isLogin ? t('welcomeBack') : t('joinUs') }}</text>
            </view>
            
            <!-- 表单区域 -->
            <view class="form-wrapper">
                <form>
                <!-- 手机号输入框 -->
                <view class="input-item">
                    <text class="iconfont icon-phone"></text>
                    <input 
                        type="number" 
                        v-model="form.phonenumber" 
                        :maxlength="11" 
                        :placeholder="t('phonePlaceholder')" 
                        placeholder-class="placeholder"
                    />
                </view>
                <!-- 密码输入框 -->
                <view class="input-item">
                        <text class="iconfont icon-lock"></text>
                        <input 
                            type="safe-password" 
                            v-model="form.password" 
                            :placeholder="t('passwordPlaceholder')" 
                            placeholder-class="placeholder"
                        />
                </view>
                                
                <!-- 注册时显示的额外字段 -->
                <template v-if="!isLogin"> 

                    <view class="input-item">
                        <text class="iconfont icon-lock"></text>
                        <input 
                            type="safe-password" 
                            v-model="form.confirmPassword" 
                            :placeholder="t('confirmPasswordPlaceholder')" 
                            placeholder-class="placeholder"
                        />
                    </view>                    
                    
                    <view class="input-item">
                        <text class="iconfont icon-user"></text>
                        <input 
                            type="text" 
                            v-model="form.username" 
                            :placeholder="t('usernamePlaceholder')" 
                            placeholder-class="placeholder"
                        />
                    </view>

                </template>

                    <view class="input-item code-item" v-if="!useCaptcha">
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

                    <!--弹出的图形验证码-->
                    <view class="input-item code-item" v-else>
                        <text class="iconfont icon-safe"></text>
                        <input 
                            type="text" 
                            v-model="form.verifyCode" 
                            :maxlength="6" 
                            :placeholder="t('captchaPlaceholder')" 
                            placeholder-class="placeholder"
                        />
                        <wd-img 
                        class="code-img" 
                        radius="10" 
                        :src="captchaStore.codeImgUrl" 
                        @tap="refreshCaptcha">
                            <template #error>
                                <view class="error-wrap">{{ t('captchaLoadError') }}</view>
                            </template>
                            <template #loading>
                                <view class="loading-wrap">
                                    <wd-loading />
                                </view>
                            </template>
                        </wd-img>
                    </view>


                </form>
            </view>
            
            <!-- 操作按钮区 -->
            <view class="action-wrapper">
                <button class="submit-btn" @tap="handleSubmit">
                    {{ isLogin ? t('loginLabel') : t('registerLabel') }}
                </button>
                <view class="switch-wrapper">
                    <text v-if="isLogin" class="forget-pwd" @tap="goToForgetPassword">{{ t('forgotPasswordLabel') }}</text>
                    <view class="switch-box">
                        <text class="switch-tip">{{ isLogin ? t('noAccount') : t('haveAccount') }}</text>
                        <text class="switch-btn" @tap="switchLoginType">
                            {{ isLogin ? t('registerNow') : t('goToLogin') }}
                        </text>
                    </view>
                </view>
                
                <!-- 隐私协议 -->
                <view class="privacy-agreement">
                    <checkbox-group @change="handlePrivacyChange">
                        <checkbox :checked="agreePrivacy" style="transform:scale(0.7)" />
                    </checkbox-group>
                    <text class="agreement-text">{{ t('agreePrivacyPolicy') }}</text>
                    <text class="agreement-link" @tap="showPrivacyPolicy">{{ t('privacyPolicy') }}</text>
                </view>
                <view class="changelanguage">
                    <wd-button 
                        size="small" 
                        icon="internet" 
                        plain 
                        @tap="changeLanguage"
                    >
                        change Language
                    </wd-button>
                </view>
                <!--语言选择器-->
		        <LanguageSelector ref="langSelectorRef" />
            </view>
        </view>
    </view>
</template>

<script setup lang="ts">
import { getUserApi, loginApi, registerApi } from '@/api/loginApi';
import LanguageSelector from '@/components/language-selector.vue';
import { useUserStore } from '@/store';
import { useCaptchaStore } from '@/store/captchaStore';
import { storeToRefs } from 'pinia';
import { inject, onBeforeUnmount, reactive, ref } from 'vue';

const t = inject('t') as (key: string) => string;
if (!t) {
    throw new Error("Localization function 't' is not provided. Ensure it is injected properly.");
}

//图形验证码缓存
const captchaStore = useCaptchaStore()

const langSelectorRef = ref()

const store = useUserStore()
const { userInfo } = storeToRefs(store)

const isLogin = ref(true)
const form = reactive({
    username: '',
    phonenumber: '',
    verifyCode: '',
    password: '',
    confirmPassword: '',
    uuid:''
})
const counting = ref(false)
const counter = ref(60)
const agreePrivacy = ref(false)
let timer: ReturnType<typeof setInterval> | null = null

//控制是否显示图形验证码
const useCaptcha = ref(true)

function switchLoginType() {
    isLogin.value = !isLogin.value
    // 重置表单
    form.username = ''
    form.phonenumber = ''
    form.verifyCode = ''
    form.password = ''
    form.confirmPassword = ''
    // 重置验证码状态
    if (counting.value && timer) {
        clearInterval(timer)
        counting.value = false
        counter.value = 60
    }
}


const captchaFetched = ref(false)

// 页面加载时请求一次验证码
onMounted(() => {
    if (!captchaFetched.value && !captchaStore.codeImgUrl) {
        captchaFetched.value = true
        console.log('获取图形验证码')
        captchaStore.fetchCaptcha().then(() => {
            form.uuid = captchaStore.uuid;
            //console.log('图形验证码UUID:', form.uuid)
        })       
        
    }
})


//刷新图形验证码
function refreshCaptcha() {
    captchaStore.fetchCaptcha().then(() => {
        form.uuid = captchaStore.uuid;
    })      
}

function getVerifyCode() {
    if (counting.value) return

    if (!form.phonenumber) {
        uni.showToast({
            title: t('enterPhoneNumber'),
            icon: 'none'
        })
        return
    }

    if (!/^1[3-9]\d{9}$/.test(form.phonenumber)) {
        uni.showToast({
            title: t('invalidPhoneNumber'),
            icon: 'none'
        })
        return
    }

    console.log('获取验证码：', form.phonenumber)

    // 开始倒计时
    counting.value = true
    counter.value = 60
    timer = setInterval(() => {
        counter.value--
        if (counter.value <= 0 && timer) {
            clearInterval(timer)
            counting.value = false
        }
    }, 1000)

    uni.showToast({
        title: t('verificationCodeSent'),
        icon: 'success'
    })
}

//显示隐私协议
function showPrivacyPolicy() {
    uni.showToast({
        title: t('privacyPolicyText'),
        icon: 'none',
        duration: 3000
    })
}

function handlePrivacyChange(e: any) {
    agreePrivacy.value = e.detail.value.length > 0
}

function goToForgetPassword() {
    uni.navigateTo({
        url: './forget-password'
    })
}

const isSubmitting = ref(false)

function changeLanguage() {
    console.log('切换语言')
    if (langSelectorRef.value) {
		langSelectorRef.value.show = true;
	}
}

const handleSubmit = async () => {

    if (!agreePrivacy.value) {
        uni.showToast({
            title: t('agreePrivacyPolicyFirst'),
            icon: 'none'
        })
        return
    }

    if (!form.phonenumber || !/^1[3-9]\d{9}$/.test(form.phonenumber)) {
        uni.showToast({
            title: t('invalidPhoneNumber'),
            icon: 'none'
        })
        return
    }
    
    if (!form.password) {
        uni.showToast({
            title: t('enterPassword'),
            icon: 'none'
        })
        return
    }

    if (!form.verifyCode) {
        uni.showToast({
            title: t('enterVerificationCode'),
            icon: 'none'
        })
        return
    }

    if(!isLogin){
        // 注册验证
            if (!form.username) {
                uni.showToast({
                    title: t('enterUsername'),
                    icon: 'none'
                })
                return
            }

            if (!form.password) {
                uni.showToast({
                    title: t('enterPassword'),
                    icon: 'none'
                })
                return
            }

            if (!form.confirmPassword) {
                uni.showToast({
                    title: t('confirmPasswordPrompt'),
                    icon: 'none'
                })
                return
            }

            if (form.password !== form.confirmPassword) {
                uni.showToast({
                    title: t('passwordMismatch'),
                    icon: 'none'
                })
                return
            }
    }
    
    // 防止重复提交
    if (isSubmitting.value) return
        isSubmitting.value = true

    try{ 

        if (isLogin.value) {
            form.username=form.phonenumber // 登录时使用手机号作为用户名
            //提交登陆
            //调用loginApi提交登录并显示返回信息
            const loginRes = await loginApi({
                username: form.username,
                password: form.password,
                code: form.verifyCode,
                uuid: form.uuid,
            })

            if (loginRes.code === 200) {
                uni.showToast({
                    title: t('loginSuccess'),
                    icon: 'success',
                })

                // 保存token
                store.setUserInfo({
                    accessToken: loginRes.access_token,
                    refreshToken: loginRes.refresh_token,
                })

                // 等待token设置后再请求用户信息
                const userRes = await getUserApi()
                if (userRes.code === 200) {
                    store.setUserInfo(userRes.user)
                    store.setUserInfo({ roles: userRes.roles })

                    uni.switchTab({
                        url: '/pages/index/index',
                    })
                } else {
                    uni.showToast({
                        title: t('getUserInfoFailed'),
                        icon: 'error',
                    })
                }
            } else {
                uni.showToast({
                title: t('loginFailed') + "," + loginRes.msg,
                icon: 'error',
                })
                refreshCaptcha()
            }
        } else {            
            //提交注册
            //调用registerApi提交注册并显示返回信息
            registerApi({
                username: form.username,
                phonenumber: form.phonenumber,
                code: form.verifyCode,
                password: form.password,
                confirmPassword: form.confirmPassword,
                uuid: form.uuid
            }).then((res) => {
                if (res.code === 200) {
                    uni.showToast({
                        title: t('registrationSuccess'),
                        icon: 'success'
                    })
                    // 清空表单
                    form.username = ''
                    form.phonenumber = ''
                    form.verifyCode = ''
                    form.password = ''
                    form.confirmPassword = ''
                    form.uuid = ''
                    //注册成功后跳转首页
                    uni.switchTab({
                        url: '/pages/index/index'
                    })
                } else {
                    uni.showToast({
                        title: t('registrationFailed') + "," + res.msg,
                        icon: 'error'
                    })
                    //刷新验证码
                    refreshCaptcha()
                }
            })

        }
    } finally {
        isSubmitting.value = false
  }

}

// 组件卸载时清理定时器
onBeforeUnmount(() => {
    if (timer) {
        clearInterval(timer)
    }
})

// 设置页面标题
onMounted(() => {
  uni.setNavigationBarTitle({
    title: t('NavigationTitle') // Use the injected 't' function for localization
  });
});

</script>

<style lang="scss" scoped>
.login-container {
    min-height: 100vh;
    background: #f8f9fd;
    position: relative;
    overflow: hidden;
}

/* 背景动画 */
.bg-animation {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1;
    
    .circle {
        position: absolute;
        border-radius: 50%;
        animation: float 15s infinite;
        
        &-1 {
            width: 300rpx;
            height: 300rpx;
            background: linear-gradient(45deg, #fbba0a 0%, #fad0c4 99%, #fad0c4 100%);
            top: -100rpx;
            right: -50rpx;
            animation-delay: 0s;
        }
        
        &-2 {
            width: 200rpx;
            height: 200rpx;
            background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
            bottom: 10%;
            left: -50rpx;
            animation-delay: -5s;
        }
        
        &-3 {
            width: 400rpx;
            height: 400rpx;
            background: linear-gradient(to top, #10d5f7 0%, #73c8e2 100%);
            bottom: -150rpx;
            right: -100rpx;
            animation-delay: -10s;
        }
    }
}

@keyframes float {
    0%, 100% {
        transform: translateY(0) rotate(0deg);
    }
    50% {
        transform: translateY(-20rpx) rotate(10deg);
    }
}

/* 主内容区 */
.content-wrapper {
    position: relative;
    z-index: 2;
    padding: 60rpx 40rpx;
}

/* Logo区域 */
.logo-box {
    text-align: center;
    margin: 60rpx 0 80rpx;
    
    .logo-text {
        font-size: 48rpx;
        font-weight: 600;
        background: linear-gradient(45deg, #f7bd58 0%, #c4ebfa 99%, #f84a4a 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        display: block;
        margin-bottom: 20rpx;
    }
    
    .sub-title {
        font-size: 28rpx;
        color: #666;
    }
}

/* 表单样式 */
.form-wrapper {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 30rpx;
    padding: 40rpx;
    box-shadow: 0 20rpx 40rpx rgba(0, 0, 0, 0.05);
    backdrop-filter: blur(10px);
    
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
            color: #2580db;
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
            color: #2147ed;
            
            &.disabled {
                color: #999;
            }
        }
        .code-img {
            position: absolute;
            right: 10rpx;
            width: 220rpx;
            height: 80rpx;
        }
    }
}

/* 按钮区域 */
.action-wrapper {
    margin-top: 60rpx;
    
    .submit-btn {
        width: 100%;
        height: 90rpx;
        line-height: 90rpx;
        background: linear-gradient(45deg, #8cafd1 0%, #3280ed 100%);
        border-radius: 45rpx;
        color: #fff;
        font-size: 32rpx;
        font-weight: 500;
        letter-spacing: 4rpx;
        border: none;
        
        &:active {
            transform: scale(0.98);
        }
    }
    
    .switch-wrapper {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 40rpx;
        padding: 0 20rpx;
        
        .forget-pwd {
            font-size: 26rpx;
            color: #377bf0;
        }
        
        .switch-box {
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
    }
    
    .privacy-agreement {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24rpx;
        margin-top: 30rpx;
        
        .agreement-text {
            color: #666;
            margin-right: 5rpx;
        }
        
        .agreement-link {
            color: #1376f0;
        }
    }

    .changelanguage{
        display: flex;
        justify-content: center;
        margin-top: 20rpx;
    }
}
</style> 