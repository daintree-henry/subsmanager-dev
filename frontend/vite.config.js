import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    watch: {
      usePolling: true
    }
  },
  resolve: {
    alias: [
      {
        find: '@',
        replacement: '/app/src'
      }
    ]
  },
  logLevel: 'debug',  // 'info' | 'warn' | 'error' | 'silent'
  customLogger: {
    debug: (msg) => console.log(`[Vite debug] ${msg}`),
    info: (msg) => console.log(`[Vite Info] ${msg}`),
    warn: (msg) => console.warn(`[Vite Warning] ${msg}`),
    error: (msg) => console.error(`[Vite Error] ${msg}`)
  }
})