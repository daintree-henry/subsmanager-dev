<template>
 <div class="flex flex-col min-h-screen">
   <nav v-if="auth.isAuthenticated" class="bg-white border-b border-gray-200 fixed top-0 w-full z-50">
     <div class="max-w-7xl mx-auto">
       <div class="flex justify-between items-center h-20 px-6">
          <div class="flex items-center space-x-12">
            <div class="flex-shrink-0">
              <span class="text-3xl font-black bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-indigo-800">
                SUBS MANAGER
              </span>
            </div>
            <div class="hidden md:flex space-x-1">
              <router-link
                to="/"
                class="relative px-5 py-2.5 rounded-xl text-base font-medium transition-all duration-200 group"
                :class="[$route.path === '/' ? 'text-indigo-700' : 'text-gray-600 hover:text-indigo-600']"
              >
                <span class="relative z-10">HOME</span>
                <div v-show="$route.path === '/'" class="absolute inset-0 bg-indigo-50 rounded-xl"></div>
              </router-link>
              <router-link
                to="/plans"
                class="relative px-5 py-2.5 rounded-xl text-base font-medium transition-all duration-200 group"
                :class="[$route.path === '/plans' ? 'text-indigo-700' : 'text-gray-600 hover:text-indigo-600']"
              >
                <span class="relative z-10">PLANS</span>
                <div v-show="$route.path === '/plans'" class="absolute inset-0 bg-indigo-50 rounded-xl"></div>
              </router-link>
              <router-link
                to="/payments"
                class="relative px-5 py-2.5 rounded-xl text-base font-medium transition-all duration-200 group"
                :class="[$route.path === '/payments' ? 'text-indigo-700' : 'text-gray-600 hover:text-indigo-600']"
              >
                <span class="relative z-10">PAYMENTS</span>
                <div v-show="$route.path === '/payments'" class="absolute inset-0 bg-indigo-50 rounded-xl"></div>
              </router-link>
            </div>
          </div>
         <div class="flex items-center space-x-6">
            <div class="relative">
              <div @click="isProfileOpen = !isProfileOpen" class="flex items-center space-x-3 cursor-pointer">
                <div class="text-right">
                  <p class="text-sm font-medium text-gray-700">{{ auth.user?.full_name || 'Guest' }}</p>
                </div>
                <div class="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center">
                  <span class="text-indigo-600 font-medium">
                    {{ auth.user?.username ? auth.user.username.charAt(0).toUpperCase() : 'U' }}
                  </span>
                </div>
              </div>

              <!-- 드롭다운 메뉴 -->
              <div
                v-if="isProfileOpen"
                class="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-lg py-2 border border-gray-100"
              >
                <div class="px-4 py-3 border-b border-gray-100">
                  <p class="text-sm font-medium text-gray-700">{{ auth.user?.username }}</p>
                  <p class="text-xs text-gray-500 truncate">{{ auth.user?.email }}</p>
                </div>
                <button @click="handleLogout" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-50">
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
   <main class="flex-1 bg-gradient-to-br from-gray-50 to-gray-100">
     <div class="max-w-7xl w-full mx-auto">
       <router-view v-slot="{ Component }">
         <transition name="fade" mode="out-in" :key="$route.path">
           <component :is="Component"/>
         </transition>
       </router-view>
     </div>
   </main>


   <footer class="bg-white border-t border-gray-200 fixed bottom-0 w-full">
     <div class="max-w-7xl mx-auto py-2 px-6">
       <div class="flex flex-col md:flex-row justify-between items-center">
         <div class="flex items-center space-x-2 text-gray-600">
           <span>&copy; {{ currentYear }}</span>
           <span class="font-semibold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-indigo-800">
             DevWiki
           </span>
           <span>All rights reserved.</span>
         </div>
       </div>
     </div>
   </footer>
 </div>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'
import { ref, onMounted, computed, nextTick } from 'vue'

const auth = useAuthStore()
const router = useRouter()
const currentYear = ref(new Date().getFullYear())
const isProfileOpen = ref(false)

const user = computed(() => auth.user)

onMounted(async () => {
  if (auth.token && (!auth.user || Object.keys(auth.user).length === 0)) {
    await auth.fetchUser()
  }
})

const toggleProfileMenu = async () => {
  isProfileOpen.value = !isProfileOpen.value
  await nextTick()
}

const handleLogout = async () => {
  isProfileOpen.value = false
  await auth.logout()
  await router.push('/login')
}
</script>

<style>
html,
body {
 height: 100%;
 margin: 0;
}

#app {
 min-height: 100vh;
 display: flex;
 flex-direction: column;
 padding-bottom: 4rem; /* Add padding to prevent content from being hidden behind footer */
}

.fade-enter-active,
.fade-leave-active {
 transition: opacity 0.3s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
 opacity: 0;
}
</style>