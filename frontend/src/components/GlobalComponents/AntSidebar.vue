<template>
    <div :class="['container', { collapsed: state.collapsed }]">
        <a-menu
            v-model:openKeys="state.openKeys"
            v-model:selectedKeys="state.selectedKeys"
            mode="inline"
            theme="light"
            :inline-collapsed="state.collapsed"
            :items="items"
        ></a-menu>
    </div>
    <div
        :style="{
            width: state.collapsed ? '60px' : '200px',
            height: '100vh',
            transition: 'width 0.3s',
        }"
    ></div>
</template>

<script lang="ts" setup>
import { reactive, watch, h } from 'vue'
import {
    MenuFoldOutlined,
    MenuUnfoldOutlined,
    TeamOutlined,
    FileOutlined,
    SnippetsOutlined,
    DesktopOutlined,
    MessageOutlined,
} from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const state = reactive({
    collapsed: true,
    selectedKeys: ['4'],
    openKeys: ['sub1'],
    preOpenKeys: ['sub1'],
})

const jump = (path: string) => {
    router.push(path)
}

const toggleCollapsed = () => {
    state.collapsed = !state.collapsed
    state.openKeys = state.collapsed ? [] : state.preOpenKeys
}

// 一定要保证key的顺序不变！
const items = reactive([
    {
        key: '0',
        icon: () => {
            if (state.collapsed) {
                return h(MenuUnfoldOutlined)
            } else {
                return h(MenuFoldOutlined)
            }
        },
        label: '展开/关闭',
        onClick: toggleCollapsed,
    },
    {
        key: '4',
        icon: () => h(DesktopOutlined),
        label: '工作台',
        onClick: () => jump('/panel'),
    },
    {
        key: '1',
        icon: () => h(FileOutlined),
        label: '文档管理',
        children: [
            {
                key: '1-1',
                label: '个人文档',
                onClick: () => jump('/documentCardsList'),
            },
            {
                key: '1-2',
                label: '企业文档',
                onClick: () => jump('/companyDocumentCardsList'),
            },
        ],
    },
    {
        key: '2',
        icon: () => h(SnippetsOutlined),
        label: '文档模板',
        onClick: () => jump('/doc/template'),
    },
    // key为 3 是企业管理
    {
        key: '3',
        icon: () => h(TeamOutlined),
        label: '我的企业',
        onClick: () => jump('/team/manage'),
    },
    // key 为 5 是聊天室
    {
        key: '5',
        icon: () => h(MessageOutlined),
        label: '企业聊天室',
        onClick: () => jump('/chat-center'),
    },
])

watch(
    () => state.openKeys,

    (_val, oldVal) => {
        state.preOpenKeys = oldVal
    }
)
</script>

<style scoped>
.container {
    position: fixed !important;
    z-index: 5000;
    height: 100%;
    min-height: 100%;
    transition: width 0.3s; /* Add transition for smooth width change */
    width: 200px; /* Default width for expanded state */
}

.container.collapsed {
    width: 60px; /* Width for collapsed state */
}

.ant-menu {
    height: 100%;
    min-height: 100%;
}
</style>
