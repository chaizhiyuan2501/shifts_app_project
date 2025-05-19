import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve("./src") // 相对路径别名配置，使用 @ 代替 src
    }
  },
  server: {
    host: '0.0.0.0',   // 必须设置！
    port: 5173,         // 可自定义端口
    strictPort: true,
    watch: {
      usePolling: true, // 必须加上这个用于 Docker 环境
    },
  },
})
