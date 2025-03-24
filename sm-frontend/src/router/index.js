import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const routes = [
    {
      path: '/',
      component: () => import('@/components/Home.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      component: () => import('@/components/LoginForm.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/plans',
      component: () => import('@/components/SubscriptionList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/payments',
      component: () => import('@/components/Payments.vue'),
      meta: { requiresAuth: true }
    }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  const requiresAuth = to.meta.requiresAuth || false
  const isLoginPage = to.path === '/login'

  console.log("Token Expired?", auth.isTokenExpired()) // 디버깅용
  console.log("Authenticated?", auth.isAuthenticated)

  // ✅ 로그인 페이지가 아닐 때만 토큰 만료 여부 체크
  if (!isLoginPage && auth.isTokenExpired()) {
    await auth.logout() // 로그아웃 처리
    return next({ path: '/login', query: { redirect: to.fullPath } })
  }

  if (requiresAuth && !auth.isAuthenticated) {
    return next({ path: '/login', query: { redirect: to.fullPath } })
  } else if (isLoginPage && auth.isAuthenticated) {
    return next({ path: '/' })
  } else {
    return next()
  }
})


export default router
