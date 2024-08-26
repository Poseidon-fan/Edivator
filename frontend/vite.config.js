import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import VueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
    // prevent vite from obscuring rust errors
    clearScreen: false,
    plugins: [vue(), VueDevTools()],
    // to access the Tauri environment variables set by the CLI with information about the current target
    envPrefix: ['VITE_', 'TAURI_PLATFORM', 'TAURI_ARCH', 'TAURI_FAMILY', 'TAURI_PLATFORM_VERSION', 'TAURI_PLATFORM_TYPE', 'TAURI_DEBUG'],
    server: {
        // Tauri expects a fixed port, fail if that port is not available
        strictPort: true,
        port: 3000, // 可选：指定开发服务器的端口
        // proxy:{
        // 	'/api':{
        // 		target:"http://127.0.0.1:8000", //跨域地址
        // 		changeOrigin:true, //支持跨域
        // 		rewrite:(path) => path.replace(/^\/api/, "")//重写路径,替换/api
        // 	}
        // }
    },
    resolve: {
        alias: {
            '@': resolve(__dirname, './src'),
            '*': resolve(''),
        },
    },
    build: {
        // Tauri uses Chromium on Windows and WebKit on macOS and Linux
        target: process.env.TAURI_PLATFORM == 'windows' ? 'chrome105' : 'safari13',
        // don't minify for debug builds
        minify: !process.env.TAURI_DEBUG ? 'esbuild' : false,
        // 为调试构建生成源代码映射 (sourcemap)
        sourcemap: !!process.env.TAURI_DEBUG,
    },
    esbuild: {
        // drop: ['console', 'debugger'],
    },
})
