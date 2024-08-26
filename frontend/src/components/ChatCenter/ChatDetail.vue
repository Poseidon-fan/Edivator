<script setup lang="ts">
import { computed, defineProps, nextTick, onMounted, ref } from 'vue'
import { CloseOutlined, SendOutlined, TeamOutlined, UsergroupAddOutlined } from '@ant-design/icons-vue'
import UserMessage from '@/components/ChatCenter/UserMessage.vue'
import api from '@/api'
import { message } from 'ant-design-vue'
import { useProfileStore } from '@/store/profile'
import { format } from 'date-fns'
import teamAvatar from '@/assets/images/teamAvatar.png'

const props = defineProps({
    group: {
        type: Object as () => { name: string; avatar: string; id: number },
        required: false,
    },
})

const groupUsers = ref([])

const requests = ref([])

const profile = useProfileStore()

const searchInfo = ref('')

const filteredUsers = computed(() => {
    const searchLower = searchInfo.value.toLowerCase()
    return groupUsers.value.filter((user) => user.username.toLowerCase().includes(searchLower))
})
const queryGroupUsers = async () => {
    toolName.value = '群组成员'
    showRightTools.value = true
    groupUsers.value = await api.get(props.group.id)
}

const handleAddUser = async () => {
    toolName.value = '申请列表'
    showRightTools.value = true
    const res = await api.getApplications(props.group?.id)
    if (res != null) {
        requests.value = res
    } else {
        message.warn('非群主无权查看')
    }
}

const handleAccept = async (requestId: number) => {
    const res = await api.handleApplication({
        app_id: requestId,
        judge: true,
    })
    if (res != null) {
        // requests里删除
        requests.value = requests.value.filter((request: any) => request.id != requestId)
        message.success('已同意申请')
    } else {
        message.error('处理时遇到问题')
    }
}

const handleReject = async (requestId: number) => {
    const res = await api.handleApplication({
        app_id: requestId,
        judge: false,
    })
    if (res != null) {
        requests.value = requests.value.filter((request: any) => request.id != requestId)
        message.success('已拒绝申请')
    } else {
        message.error('处理时遇到问题')
    }
}

const messages = ref<any[]>([])

const ws = ref<any>(null)
const curMessage = ref({
    text: '',
    image: '',
    sender: profile.id,
    group: props.group?.id,
})
const connected = ref(false)

const connectWebSocket = () => {
    if (ws.value) {
        ws.value.close()
    }

    const websocketUrl = `ws://101.201.173.118:8000/ws/chat/${props.group.id}/?user_id=${profile.id}`
    ws.value = new WebSocket(websocketUrl)

    ws.value.onopen = () => {
        console.log('WebSocket connected')
        connected.value = true
    }

    ws.value.onmessage = (event: any) => {
        const data = JSON.parse(event.data)
        data.isSelf = data.sender.id == profile.id
        messages.value.push(data)
        setTimeout(() => {
            if (chatContentRef.value) {
                chatContentRef.value.scrollTop = chatContentRef.value.scrollHeight
            }
        }, 100)
    }

    ws.value.onclose = () => {
        connected.value = false
    }

    ws.value.onerror = (error: any) => {
        console.error('WebSocket error:', error)
        connected.value = false
    }
}

const sendMessage = async () => {
    if (!curMessage.value.text && !curMessage.value.image) {
        message.warn('内容不能为空')
    } else {
        await ws.value.send(JSON.stringify(curMessage.value))
        setTimeout(() => {
            scrollToBottom()
        }, 100)

        curMessage.value = {
            text: '',
            image: '',
            sender: profile.id,
            group: props.group?.id,
        }
    }
}

const chatContentRef = ref(null)

const handleKeyDown = (event: any) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault()
        sendMessage()
    }
}

const scrollToBottom = () => {
    if (chatContentRef.value) {
        chatContentRef.value.scrollTop = chatContentRef.value.scrollHeight
    }
}

const delayScrollDown = () => {
    setTimeout(() => {
        if (chatContentRef.value) {
            chatContentRef.value.scrollTop += 130
        }
    }, 100)
}

onMounted(async () => {
    const tmp = await api.getMessages(props.group.id)
    tmp.forEach((message) => {
        message.isSelf = message.sender.id == profile.id
    })
    messages.value = tmp

    await nextTick()
    scrollToBottom()
    connectWebSocket()
})

const formatDate = (dateStr: string) => {
    return format(new Date(dateStr), 'yyyy-MM-dd')
}

const formatTime = (dateStr: string) => {
    return format(new Date(dateStr), 'HH:mm:ss')
}

const showRightTools = ref(false)
const toolName = ref('')

const handleDeleteImage = () => {
    curMessage.value.image = null
}
</script>

<template>
    <div class="outer-container">
        <div class="chat-detail-container">
            <div class="chat-header">
                <div class="chat-title">
                    <a-avatar class="teamAvatar" :src="group?.avatar ? group?.avatar : teamAvatar" size="large" />
                    <h2>{{ group?.name }}</h2>
                    <a-tooltip>
                        <template #title>查看群成员</template>
                        <div @click="queryGroupUsers">
                            <TeamOutlined style="font-size: 15px" />
                        </div>
                    </a-tooltip>
                </div>
                <div class="header-right">
                    <div class="tool-list">
                        <a-tooltip>
                            <template #title>添加群成员</template>
                            <div class="tool-item" @click="handleAddUser">
                                <UsergroupAddOutlined style="font-size: 20px" />
                            </div>
                        </a-tooltip>
                    </div>
                </div>
            </div>

            <div class="chat-content" ref="chatContentRef">
                <div v-for="message in messages" :key="message.id">
                    <UserMessage :message="message" @notify="delayScrollDown" />
                </div>
            </div>

            <div class="chat-input">
                <div class="chat-image" v-if="curMessage.image != ''">
                    <img :src="curMessage.image" alt="发送的表情" class="image-preview" />
                    <CloseOutlined class="delete-icon" @click="handleDeleteImage" />
                </div>
                <a-textarea
                    v-model:value="curMessage.text"
                    :placeholder="'发送到 ' + group?.name"
                    size="large"
                    @keydown="handleKeyDown"
                    :autoSize="{ maxRows: 4 }"
                ></a-textarea>
                <div class="emit" @click="sendMessage">
                    <SendOutlined style="color: #1890ff; font-size: 24px" />
                </div>
            </div>
        </div>
        <div class="right-tools" v-if="showRightTools">
            <div class="tools-header">
                <h3>{{ toolName }}</h3>
                <div class="close-tools" @click="showRightTools = false">
                    <CloseOutlined />
                </div>
            </div>
            <div v-if="toolName == '群组成员'">
                <div class="users-list">
                    <div style="margin: 10px 0">
                        <a-input-search v-model:value="searchInfo" placeholder="搜索群成员" />
                        <div v-for="user in filteredUsers" :key="user.id" class="users-list-item">
                            <a-avatar :src="user.avatar" />
                            <span>{{ user.username }}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else-if="toolName == '申请列表'">
                <a-list item-layout="horizontal" :dataSource="requests" class="request-list">
                    <template #renderItem="{ item }">
                        <a-list-item class="request-item">
                            <a-list-item-meta>
                                <template #avatar>
                                    <a-avatar :src="item.applicant.avatar" />
                                </template>
                                <template #title>
                                    <div class="applicant-info">
                                        <span class="username">{{ item.applicant.username }}</span>
                                        <div class="time-info">
                                            <span>{{ formatDate(item.created_at) }}</span>
                                            <span>{{ formatTime(item.created_at) }}</span>
                                        </div>
                                    </div>
                                </template>
                            </a-list-item-meta>
                            <div class="actions">
                                <a-button type="primary" size="small" class="agree-btn" @click="handleAccept(item.id)">
                                    同意
                                </a-button>
                                <a-button type="default" size="small" class="reject-btn" @click="handleReject(item.id)">
                                    拒绝
                                </a-button>
                            </div>
                        </a-list-item>
                    </template>
                </a-list>
            </div>
        </div>
    </div>
</template>

<style scoped>
.outer-container {
    display: flex;
    height: 100%;
}

.chat-detail-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
}

.right-tools {
    width: 500px;
    border-left: 1px solid #e8e8e8;
    margin-left: 2px;
    padding: 20px;
}

.chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #e8e8e8;
}

.chat-title {
    display: flex;
    align-items: center;
}

.header-right {
    margin-left: auto;
}

.tool-list {
    margin-right: 10px;
}

.tool-item {
    padding: 5px;
}

.tool-item:hover {
    background-color: rgb(200, 200, 200);
    border-radius: 5px;
    cursor: pointer;
}

.chat-content {
    flex: 1;
    padding: 10px;
    overflow-y: auto;
}

.chat-input {
    padding: 10px;
    border-top: 1px solid #e8e8e8;
    display: flex;
    align-items: center;
    position: relative;
}

h2 {
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-left: 10px;
    margin-top: 7px;
    font-weight: bold;
    font-size: 1.2em;
}

.chat-title > div {
    cursor: pointer;
    margin-left: 10px;

    :hover {
        color: #1890ff;
    }
}

.emit {
    margin-left: 10px;
    cursor: pointer;
}

.tools-header {
    display: flex;
    justify-content: space-between;
    width: 100%;
    border-bottom: 1px solid #e8e8e8;
}

.close-tools {
    cursor: pointer;
}

.request-list {
    padding: 12px;
    background-color: #f0f8ff;
}

.request-item {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.applicant-info {
    display: flex;
    flex-direction: column;
}

.username {
    font-weight: 600;
    color: #333;
}

.time-info {
    margin-top: 4px;
    color: #666;
    font-size: 12px;
}

.actions {
    display: flex;
    gap: 8px;
}

.users-list-item {
    padding: 10px;
    width: 100%;
    display: flex;
    align-items: center;
    margin-top: 5px;
}

.users-list-item:hover {
    background-color: #40a9ff20;
    border-radius: 10px;
}

.users-list-item > span {
    margin-left: 10px;
    font-size: 14px;
    font-weight: 700;
}

.agree-btn {
    background-color: #40a9ff;
    border-color: #40a9ff;
}

.agree-btn:hover,
.agree-btn:focus {
    background-color: #69c0ff;
    border-color: #69c0ff;
}

.reject-btn {
    color: #ff7875;
    border-color: #ff7875;
}

.reject-btn:hover,
.reject-btn:focus {
    color: #ff9c91;
    border-color: #ff9c91;
}

.chat-content::-webkit-scrollbar {
    width: 6px; /* 滚动条宽度 */
    transition: opacity 0.3s ease-in-out; /* 滚动条显示隐藏过渡 */
    opacity: 0; /* 默认隐藏滚动条 */
}

.chat-content:hover::-webkit-scrollbar,
.chat-content:active::-webkit-scrollbar {
    opacity: 1; /* 鼠标悬停和激活时显示滚动条 */
}

.chat-content::-webkit-scrollbar-track {
    background: #ffffff; /* 滚动条轨道背景色为白色 */
    border-radius: 3px; /* 滚动条轨道圆角 */
    box-shadow: inset 0 0 3px rgba(0, 0, 0, 0.1); /* 滚动条轨道内阴影 */
}

.chat-content::-webkit-scrollbar-thumb {
    background: linear-gradient(45deg, #6a5acd, #00bfff); /* 蓝紫渐变色滑块背景 */
    border-radius: 3px; /* 滚动条滑块圆角 */
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.5); /* 滑块阴影 */
    transition: background 0.3s ease-in-out; /* 滑块背景色过渡 */
}

.chat-content::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(45deg, #00bfff, #6a5acd); /* 悬停时渐变色反转 */
}

.chat-content::-webkit-scrollbar-thumb:active {
    background: linear-gradient(45deg, #00bfff, #6a5acd); /* 激活时渐变色反转 */
    animation: pulse 1s infinite; /* 激活时脉冲动画 */
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 5px rgba(0, 191, 255, 0.5);
    }
    50% {
        box-shadow: 0 0 10px rgba(0, 191, 255, 1);
    }
    100% {
        box-shadow: 0 0 5px rgba(0, 191, 255, 0.5);
    }
}

.chat-image {
    width: 100px;
    position: absolute;
    bottom: 70px;
    padding: 5px;
    border-radius: 10px;
    background: rgba(24, 144, 255, 0.5);

    box-shadow: 0 4px 20px rgba(74, 144, 228, 0.2);
    transition: transform 0.3s, box-shadow 0.3s;
}

.chat-image:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 30px rgba(74, 144, 228, 0.4);
}

.image-preview {
    max-width: 100%;
    max-height: 100px;
    border-radius: 8px;
    border: 2px solid #4a90e2;
}

.delete-icon {
    position: absolute;
    top: 5px;
    right: 5px;
    color: white;
    cursor: pointer;
    font-size: 20px;
}

.teamAvatar {
    position: relative;
    border: solid 1px rgba(0, 0, 0, 0.4);
}
</style>
