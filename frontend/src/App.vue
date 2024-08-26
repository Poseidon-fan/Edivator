<template>
    <v-app>
        <v-main>
            <ChatButton v-if="showAiChat" />
            <Header />
            <div class="flex-container">
                <div v-show="showSidebar">
                    <Sidebar class="side-bar" />
                </div>
                <div class="view">
                    <router-view />
                </div>
            </div>
        </v-main>
    </v-app>
</template>

<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'
import Header from '@/components/GlobalComponents/GlobalHeader.vue'
import Sidebar from '@/components/GlobalComponents/AntSidebar.vue'
import Methods from '@/utils/UtilMethod'
const ChatButton = defineAsyncComponent(() => import('@/components/AI/ChatButton.vue'))

const vueRouter = useRoute()
// 跳转到主页面
if (sessionStorage.getItem('preRoute')) Methods.jump(sessionStorage.getItem('preRoute'))
else Methods.jump('/loginRegister')

// 控制Sidebar的显示与隐藏
const showSidebar = computed(() => {
    return (
        vueRouter.path !== '/loginRegister' &&
        vueRouter.path !== '/home' &&
        vueRouter.path !== '/modify' &&
        !vueRouter.path.includes('/editor/')
    )
})

const showAiChat = computed(() => {
    return vueRouter.path !== '/loginRegister' && vueRouter.path !== '/home' && vueRouter.path !== '/modify'
})
</script>

<style scoped>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}

.side-bar {
    height: 100vh;
    min-height: 100%;
    min-width: 50px !important; /*覆盖ant之前的width */
}

.view {
    margin-top: 50px; /* 保留原有的顶部间距 */
    flex: 1; /* 让 view 部分占据剩余的全部宽度和高度 */
    /* height: calc(100vh - 50px); */
}

.flex-container {
    display: flex;
}
</style>
