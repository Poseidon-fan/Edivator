<template>
    <a-list :dataSource="logs" split itemLayout="horizontal">
        <template #renderItem="{ item }">
            <a-list-item class="log-item" @click="jump(item)">
                <a-list-item-meta>
                    <template #avatar>
                        <a-avatar
                            :src="item.user.avatar ? env.backEnd.slice(0, -1) + item.user.avatar : avatar"
                            class="log-avatar"
                        />
                    </template>
                    <template #title>
                        <div class="log-meta-title">
                            <span class="log-username">{{ item.user.username }}</span>
                            <a-tag :bordered="false" :color="getActionColor(item.action)" class="log-action"
                                >{{ getActionName(item.action) }}
                            </a-tag>
                            <span class="log-time">{{ formatTime(item.time) }}</span>
                        </div>
                    </template>
                    <template #description>
                        <div class="log-document">
                            {{ item.document.name }}
                        </div>
                    </template>
                </a-list-item-meta>
            </a-list-item>
        </template>
    </a-list>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import { ElMessage } from 'element-plus'
import router from '@/router'
import env from '@/utils/env'
import avatar from '@/assets/Global/avatar.jpg'
const props = defineProps<{
    logs: Array<Log>
}>()

console.log(`output->props.logs`, props)
type Log = {
    id: number
    user: {
        id: number
        username: string
        email: string
        mobile: string | null
        avatar: string
    }
    time: string
    action: number
    document_type: number
    owner_id: number
    document: {
        id: number
        user: number | null
        team: number | null
        company: number | null
        template: number | null
        create_time: string
        update_time: string
        is_delete: boolean
        name: string
        description: string
        owner: number
        avatar: string
        version_counts: number
        creator: number
    }
    version: null
}
// 写死的数据对象

const formatTime = (time: string) => {
    const date = new Date(time)
    return date.toLocaleDateString()
}

const getActionColor = (action) => {
    const actions = {
        1: 'green',
        2: 'orange',
        3: 'red',
        4: 'cyan',
        5: 'blue',
        6: 'pink',
    }
    console.log(action)
    return actions[action] || 'gray'
}

const getActionName = (action) => {
    const actions = {
        1: '创建文档',
        2: '更新文档',
        3: '删除文档',
        4: '创建版本',
        5: '更新版本',
        6: '删除版本',
    }
    return actions[action] || '未知操作'
}

const jump = (item) => {
    if (item.document['is_delete']) ElMessage.error('文档已被删除')
    else router.push(`/editor/${item.document.id}`)
}
</script>

<style>
.log-card {
    max-width: 700px;
    margin: auto;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.log-item {
    display: flex;
    cursor: pointer;
    align-items: flex-start;
    margin-bottom: 16px;
    border-bottom: 1px solid #eaeaea;
    padding-bottom: 16px;
    transition: background-color 0.3s;
}

.log-item:hover {
    background-color: #f0f0f0;
}

.log-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-right: 16px;
}

.log-meta-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.log-username {
    font-weight: bold;
    font-size: 16px;
    color: #333;
    margin-right: 8px;
}

.log-time {
    color: #999;
    margin-left: auto;
    font-size: 14px;
}

.log-document {
    margin-top: 8px;
    padding: 8px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    color: #333;
}
</style>
