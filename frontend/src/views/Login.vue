<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-500 rounded-2xl mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-900">快传</h1>
        <p class="text-gray-500 mt-2">简单快速的文件传输工具</p>
      </div>

      <!-- 登录表单 -->
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- 邮箱输入 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="请输入邮箱"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
          />
        </div>

        <!-- 验证码输入 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">验证码</label>
          <div class="flex gap-3">
            <input
              v-model="code"
              type="text"
              required
              maxlength="6"
              placeholder="请输入验证码"
              class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
            />
            <button
              type="button"
              @click="sendCode"
              :disabled="sending || countdown > 0"
              class="px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition whitespace-nowrap"
            >
              {{ countdown > 0 ? `${countdown}s` : '发送验证码' }}
            </button>
          </div>
        </div>

        <!-- 提交按钮 -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition font-medium"
        >
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <!-- 错误提示 -->
      <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
        {{ error }}
      </div>

      <!-- 开发提示 -->
      <div class="mt-6 p-3 bg-blue-50 border border-blue-200 rounded-lg text-blue-600 text-xs">
        <p class="font-medium mb-1">开发提示：</p>
        <p>验证码会打印到后端控制台</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { sendVerificationCode, verifyCode } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const email = ref('')
const code = ref('')
const loading = ref(false)
const sending = ref(false)
const countdown = ref(0)
const error = ref('')

// 发送验证码
const sendCode = async () => {
  if (!email.value) {
    error.value = '请输入邮箱'
    return
  }

  sending.value = true
  error.value = ''

  try {
    await sendVerificationCode(email.value)
    // 开始倒计时
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (err) {
    error.value = err.response?.data?.detail || '发送验证码失败'
  } finally {
    sending.value = false
  }
}

// 提交登录
const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    const data = await verifyCode(email.value, code.value)
    userStore.setToken(data.token)
    await userStore.fetchUser()
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>
