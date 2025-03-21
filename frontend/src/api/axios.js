import axios from 'axios'
import { API_CONFIG } from '@/config/api.config';

const createAPI = (baseURL) => {
  const api = axios.create({ baseURL })

  api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })

  return api
}

export const userAPI = createAPI(API_CONFIG.USER_URL);
export const subAPI = createAPI(API_CONFIG.SUBSCRIPTION_URL);
export const recommendAPI = createAPI(API_CONFIG.RECOMMEND_URL);
