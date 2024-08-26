<template>
    <div class="notification-dropdown">
        <div class="arrow"></div>
        <el-card class="box-card">
            <div class="close-icon" @click="hideNotificationDropdown">
                <el-icon><Close /></el-icon>
            </div>
            <el-tabs v-model="activeTab" stretch>
                <el-tab-pane name="notifications">
                    <template #label> 系统通知 </template>
                    <div class="tab-content">
                        <div
                            v-for="notification in notifications"
                            :key="notification.id"
                            class="notification-item"
                            @click="markAsRead(notification)"
                        >
                            <span v-if="!notification.is_read" class="unread-dot"></span>
                            <p>
                                {{ notification.message }}
                                <span>{{ notification.date }}</span>
                            </p>
                        </div>
                    </div>
                </el-tab-pane>
            </el-tabs>
            <div class="actions">
                <el-button type="primary" plain :icon="Check" round @click="markAllAsRead()">全部已读</el-button>
            </div>
        </el-card>
    </div>
</template>

<script setup>
import { onMounted, ref, defineEmits } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Close, Check } from '@element-plus/icons-vue'
import api from '@/api'

const router = useRouter()
const emits = defineEmits(['close', 'allMessageRead', 'unreadMessage'])

const activeTab = ref('notifications')

const notifications = ref([])

const goToMessageCenter = () => {
    router.push('/messageCenter')
}

const hideNotificationDropdown = () => {
    emits('close')
}

const markAsRead = async (notification) => {
    if (!notification.is_read) {
        try {
            await api.markAsRead({ ids: [notification.id] })
            notification.is_read = true
            console.log(`Notification ${notification.id} marked as read`)
            ElMessage.success('信息标记为已读')
            let flag = true
            for (let i = 0; i < notifications.value.length; i++) {
                if (!notifications.value[i].is_read) flag = false
            }
            if (flag) emits('allMessageRead')
            else emits('unreadMessage')
        } catch (error) {
            console.error('标记消息已读失败', error)
        }
    }
}

const markAllAsRead = async () => {
    const unreadNotifications = notifications.value.filter((notification) => !notification.is_read)

    if (unreadNotifications.length === 0) {
        ElMessage.info('没有未读消息')
        return
    }

    try {
        const ids = unreadNotifications.map((notification) => notification.id)
        await api.markAsRead({ ids })
        unreadNotifications.forEach((notification) => {
            notification.is_read = true
        })
        ElMessage.success('所有消息已标记为已读')
        emits('allMessageRead')
    } catch (error) {
        console.error('标记所有消息已读失败', error)
    }
}

onMounted(async () => {
    // 加载系统通知
    setTimeout(async () => {
        notifications.value = await api.getAllNotifications()
        let flag = true
        for (let i = 0; i < notifications.value.length; i++) {
            if (!notifications.value[i].is_read) flag = false
        }
        if (flag) emits('allMessageRead')
        else emits('unreadMessage')
        console.log(`output->notifications.value`, notifications.value)
    }, 500)
})
</script>

<style scoped>
.notification-dropdown {
    position: absolute;
    top: 70px;
    right: 12%;
    width: 400px;
    z-index: 1000;
}

.notification-item {
    color: rgb(150, 150, 150);
}

.arrow {
    position: absolute;
    top: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-bottom: 10px solid #fff;
}

.box-card {
    width: 100%;
}

.close-icon {
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}

.actions {
    margin-top: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
}

.view-more {
    text-align: center;
    padding: 10px;
    background: white;
}

.view-more a {
    color: #00b3b3;
    text-decoration: none;
}

.view-more a:hover {
    text-decoration: underline;
}

.tab-content {
    max-height: 200px;
    overflow-y: auto;
    padding-right: 10px;
}

.notification-item {
    padding: 10px;
    border-bottom: 1px solid #eee;
    cursor: pointer; /* 鼠标悬停时显示手型指针 */
}

.notification-item:last-child {
    border-bottom: none;
}

.notification-item p {
    margin: 0;
    font-size: 14px;
}

.notification-item span {
    float: left;
    color: #888;
    font-size: 12px;
}

.unread-dot {
    width: 10px;
    height: 10px;
    background-color: red;
    border-radius: 50%;
    margin-right: 10px;
    display: inline-block;
}
</style>
