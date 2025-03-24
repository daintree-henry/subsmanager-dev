import { defineStore } from 'pinia'
import { userAPI } from '@/api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token')
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    async login(email, password) {
      try {
        const response = await userAPI.post('/users/login', { email, password })
        this.token = response.data.access_token
        localStorage.setItem('access_token', this.token)
        await this.fetchUser()
        return true
      } catch (error) {
        console.error('Login failed:', error)
        return false
      }
    },

    async register(userData) {
      try {
        await userAPI.post('/users/register', userData)
        return true
      } catch (error) {
        console.error('Registration failed:', error)
        return false
      }
    },

    async fetchUser() {
      try {
        if (this.isTokenExpired()) {
          this.clearAuth()
          return
        }
        const response = await userAPI.get('/users/me')
        this.user = response.data
      } catch (error) {
        if (error.response?.status === 401) {
          this.clearAuth()
        }
        console.error('Failed to fetch user:', error)
      }
    },


    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('access_token') // 'token'이 아닌 'access_token'으로 수정
    },

    isTokenExpired() {
      if (!this.token) return true
      try {
        const payload = JSON.parse(atob(this.token.split('.')[1]))
        return payload.exp * 1000 < Date.now()
      } catch (e) {
        return true
      }
    },

    clearAuth() {
      this.token = null
      this.user = null
      localStorage.removeItem('access_token')
    }
  }
})