<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-8" style="background-color: rgb(48, 94, 155);">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 md:p-10">
      <div class="text-center mb-6">
        <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-3 tracking-tight">
          Login
        </h2>
        <p class="text-base text-gray-600">
          Sign in to your account to get started
        </p>
      </div>

      <!-- 오류 메시지 표시 -->
      <div v-if="errorMessage" class="mb-4 text-sm text-red-600 text-center bg-red-100 p-3 rounded-lg">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleSubmit" class="flex flex-col gap-6">
        <div class="space-y-2.5">
          <label for="email" class="block text-sm font-medium text-gray-700">
            Email
          </label>
          <div class="relative">
            <input
              id="email"
              v-model="email"
              type="email"
              required
              class="w-full px-4 py-3.5 text-gray-900 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-100 focus:border-indigo-500 transition-colors"
              placeholder="your@email.com"
            />
          </div>
        </div>

        <div class="space-y-2.5">
          <label for="password" class="block text-sm font-medium text-gray-700">
            Password
          </label>
          <div class="relative">
            <input
              id="password"
              v-model="password"
              type="password"
              required
              class="w-full px-4 py-3.5 text-gray-900 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-100 focus:border-indigo-500 transition-colors"
              placeholder="••••••••"
            />
          </div>
        </div>

        <button
          type="submit"
          class="w-full mt-2 px-6 py-3.5 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-100 transition-colors"
        >
          Login
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const email = ref('')
const password = ref('')
const errorMessage = ref('') // 오류 메시지 상태 추가

const handleSubmit = async () => {
  errorMessage.value = '' // 오류 메시지 초기화
  const success = await auth.login(email.value, password.value)
  if (success) {
    router.push('/')
  } else {
    errorMessage.value = 'Invalid email or password. Please try again.'
  }
}
</script>
