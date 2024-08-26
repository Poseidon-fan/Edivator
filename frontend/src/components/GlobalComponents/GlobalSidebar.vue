<template>
    <div class="sidebar">
        <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            :collapse="isCollapse"
            @open="handleOpen"
            @close="handleClose"
        >
            <el-sub-menu index="1">
                <template #title>
                    <el-icon><location /></el-icon>
                    <span>文档管理</span>
                </template>
                <el-menu-item index="1-1" @click="Methods.jump('/documentCardsList')">个人文档</el-menu-item>
                <el-menu-item index="1-2">企业文档</el-menu-item>
            </el-sub-menu>
            <el-menu-item index="2">
                <el-icon><icon-menu /></el-icon>
                <template #title>Navigator Two</template>
            </el-menu-item>
            <el-menu-item index="3" disabled>
                <el-icon><document /></el-icon>
                <template #title>Navigator Three</template>
            </el-menu-item>
            <el-menu-item index="4">
                <el-icon><setting /></el-icon>
                <template #title>Navigator Four</template>
            </el-menu-item>
            <el-menu-item index="5">
                <el-icon @click="isCollapse = !isCollapse"><document /></el-icon>
            </el-menu-item>
        </el-menu>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Document, Menu as IconMenu, Location, Setting } from '@element-plus/icons-vue'
import Methods from '@/utils/UtilMethod'

const isCollapse = ref(true)
const handleOpen = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
</script>

<style scoped>
.sidebar {
    position: fixed;
    z-index: 50000;
    width: 200px;
    top: 0;
    /* margin-top: 60px; */
}

.el-menu {
    min-height: 100vh;
    background-color: white;
}

.el-menu-vertical:not(.el-menu--collapse) {
    height: 100vh;
}

.el-menu-vertical {
    height: 100vh;
}
</style>
