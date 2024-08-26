<template>
    <div
        class="chat-message"
        :class="{ 'self-message': isSelf }"
        @mouseenter="showDate = true"
        @mouseleave="showDate = false"
    >
        <div class="avatar-wrapper">
            <a-avatar :src="message.sender.avatar ? message.sender.avatar : avatar" class="avatar" />
        </div>
        <div class="message-content-wrapper">
            <div class="message-header" :style="isSelf ? 'flex-direction: row-reverse;' : ''">
                <span class="username">{{ message.sender.username }}</span>
                <div v-show="showDate" style="margin: 0 10px">
                    <a-tooltip>
                        <template #title>{{ detailData }}</template>
                        <span class="message-date">{{ shortDate }}</span>
                    </a-tooltip>
                </div>
            </div>
            <div style="display: flex" :style="isSelf ? 'flex-direction: row-reverse;' : ''">
                <div class="message-content">
                    <a-dropdown
                        :placement="isSelf ? 'left' : 'right'"
                        trigger="click"
                        :overlayStyle="{ minWidth: '200px' }"
                    >
                        <template #overlay>
                            <a-menu style="margin: 20px">
                                <a-menu-item @click="askDialogRecognition">
                                    <SmileOutlined />
                                    <span style="margin-left: 10px">情绪识别</span>
                                </a-menu-item>
                            </a-menu>
                        </template>
                        <p
                            v-if="message.text"
                            class="content-text"
                            @mouseenter="addActive"
                            @mouseleave="removeActive"
                            :class="{ active }"
                        >
                            {{ message.text }}
                        </p>
                    </a-dropdown>
                    <a-dropdown :placement="isSelf ? 'left' : 'right'" trigger="click">
                        <template #overlay>
                            <a-menu style="margin: 20px">
                                <a-menu-item @click="downloadImg(env.backEnd + message.image.slice(1))">
                                    <DownloadOutlined />
                                    <span style="margin-left: 10px">下载</span>
                                </a-menu-item>
                                <a-menu-item
                                    @click="askAi(env.backEnd + message.image.slice(1))"
                                    :disabled="hasAskedEmojiRecognition"
                                >
                                    <RobotOutlined />
                                    <span style="margin-left: 10px">AI理解表情包</span>
                                </a-menu-item>
                            </a-menu>
                        </template>
                        <img
                            v-if="message.image != null"
                            :src="env.backEnd + message.image.slice(1)"
                            class="message-image"
                            alt="用户头像"
                        />
                    </a-dropdown>
                </div>
                <div class="ai-content" v-if="emojiRecognitionContentVisible">
                    <a-spin :spinning="emojiRecognitionContentSpinning">
                        <a-card class="ai-card custom-scrollbar">
                            <div class="text">
                                <p>{{ emojiRecognitionRenderedData }}</p>
                            </div>
                        </a-card>
                    </a-spin>
                </div>
            </div>
            <!--            <div class="dialog-recognition-container" v-if="dialogRecognitionResultVisible">-->
            <!--                <a-spin tip="loading" :spinning="dialogRecognitionResultSpinning">-->
            <!--                    <DialogRecognition :emotions="dialogRecognitionResult" />-->
            <!--                </a-spin>-->
            <!--            </div>-->
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, defineProps, ref } from 'vue'
import env from '@/utils/env'
import { DownloadOutlined, RobotOutlined, SmileOutlined } from '@ant-design/icons-vue'
import { message as AntMessage } from 'ant-design-vue'
import api from '@/api'
import avatar from '@/assets/Global/avatar.jpg'
// import DialogRecognition from '@/components/DialogRecognition.vue'

const props = defineProps<{
    message: {
        id: number
        text: string
        image: string
        sender: {
            username: string
            id: number
            avatar: string
        }
        isSelf: boolean
        created_at: string
    }
}>()
// eslint-disable-next-line vue/valid-define-emits
const emit = defineEmits()

const isSelf = computed(() => props.message.isSelf)

const downloadImg = async (imageUrl: string) => {
    try {
        const response = await fetch(imageUrl)
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = imageUrl.split('/').pop() || 'download'
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        window.URL.revokeObjectURL(url)
    } catch (error) {
        AntMessage.error('下载错误')
    }
}

const emojiRecognitionContentVisible = ref(false)
const emojiRecognitionContentSpinning = ref(false)
const emojiRecognitionContent = ref('')
const emojiRecognitionRenderedData = ref('')
const hasAskedEmojiRecognition = ref(false)

const dialogRecognitionResultVisible = ref(false)
const dialogRecognitionResultSpinning = ref(false)
const dialogRecognitionResult = ref([])
const hasAskedDialogRecognition = ref(false)

let interval: any = null
const renderEmojiRecognitionData = () => {
    let index = 0
    interval = setInterval(() => {
        if (index < emojiRecognitionContent.value.length) {
            emojiRecognitionRenderedData.value += emojiRecognitionContent.value[index]
            index++
        } else {
            clearInterval(interval)
        }
    }, 20) // 调整时间间隔以控制渲染速度
}

const askAi = async (imageUrl: string) => {
    try {
        emojiRecognitionContentVisible.value = true
        emojiRecognitionContentSpinning.value = true
        const response = await fetch(imageUrl)
        if (!response.ok) {
            AntMessage.error('网络错误')
        }
        const blob = await response.blob()
        const reader = new FileReader()
        reader.onloadend = async () => {
            const base64data = reader.result // Base64 编码数据
            // const response = await api.emoji_understand({ base64_img: base64data }, {})
            // aiContent.value = response.result
            await new Promise((resolve) => setTimeout(resolve, 5000))
            emojiRecognitionContent.value =
                '这张图片展示了一个表情痛苦的卡通人物。这个角色有一个大的球形身体，一个突出的弯曲的脊柱，一个宽而张开的嘴。角色的眼睛又宽又圆，皮肤上有水滴，表明它可能在出汗或哭泣。背景很简单，木质纹理可能是墙壁或门，蓝色色调可能表示天空或墙壁。图像中有文字，用非拉丁字母书写，似乎是中文。图像的风格是卡通的，具有典型的动画人物夸张的特征和表情。角色的情绪传达了一种恐惧或恐慌的感觉。'

            emojiRecognitionContentSpinning.value = false
            hasAskedEmojiRecognition.value = true
            renderEmojiRecognitionData()
        }
        reader.readAsDataURL(blob)
    } catch (error) {
        AntMessage.error('获取图片失败')
    }
}

const askDialogRecognition = async () => {
    try {
        dialogRecognitionResultVisible.value = true
        emit('notify')
        dialogRecognitionResultSpinning.value = true
        await new Promise((resolve) => setTimeout(resolve, 2000))
        dialogRecognitionResult.value = await api.dialogEmotionRecognition(props.message.text)
        dialogRecognitionResultSpinning.value = false
        emit('notify')
        hasAskedDialogRecognition.value = true
    } catch (error) {
        AntMessage.error('识别情绪失败')
    }
}

const formattedShortDateTime = (date: string) => {
    const dateTime = new Date(date)
    const month = dateTime.getMonth() + 1 // 月份从0开始
    const day = dateTime.getDate()
    const hour = dateTime.getHours()
    const minute = dateTime.getMinutes()

    return `${month}月${day}日 ${hour}:${minute < 10 ? '0' + minute : minute}`
}

const formattedDetailDateTime = (date: string) => {
    const dateTime = new Date(date)
    const year = dateTime.getFullYear()
    const month = dateTime.getMonth() + 1 // 月份从0开始
    const day = dateTime.getDate()
    const hour = dateTime.getHours()
    const minute = dateTime.getMinutes()
    const second = dateTime.getSeconds()

    return `${year}年${month}月${day}日 ${hour}:${minute < 10 ? '0' + minute : minute}:${
        second < 10 ? '0' + second : second
    }`
}

const shortDate = computed(() => {
    return formattedShortDateTime(props.message.created_at)
})

const detailData = computed(() => {
    return formattedDetailDateTime(props.message.created_at)
})

const showDate = ref(false)

const active = ref(false)

const addActive = () => {
    active.value = true
}

const removeActive = () => {
    active.value = false
}
</script>

<style scoped>
.chat-message {
    display: flex;
    align-items: flex-start;
    margin-bottom: 20px;
}

.chat-message.self-message {
    flex-direction: row-reverse;
    text-align: right;
}

.avatar-wrapper {
    flex-shrink: 0;
}

.avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.self-message .avatar {
    margin-left: 15px;
    margin-right: 0;
}

.message-content-wrapper {
    max-width: 70%;
}

.message-header {
    margin-bottom: 5px;
    display: flex;
    align-items: center;
}

.message-date {
    font-size: 12px;
    color: rgb(143, 149, 158);
}

.username {
    color: #333;
    font-size: 16px;
    font-weight: bold;
}

.message-content {
    background: #fff; /* 修改为白色背景 */
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 15px;
}

.self-message .message-content {
    background: #f0f0f0; /* 修改为浅灰色背景 */
}

.message-body {
    color: #555;
    font-size: 14px;
    line-height: 1.5;
}

.message-image {
    max-width: 200px;
    border-radius: 4px;
    margin-top: 10px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}

.message-image:hover {
    transform: scale(1.1); /* 放大效果 */
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
    border: 3px solid rgba(255, 215, 0, 0.8);
}

.tool-list {
    display: flex;
    flex-direction: column;
}

.tool-item {
    font-size: 15px;
    margin: 5px;
    background-color: #fafafa;
    border-radius: 5px;
}

.tool-item > span {
    margin-left: 10px;
}

.ai-content {
    height: 100%;
    margin: 0 20px;
}

.ai-card {
    width: 100%;
    max-width: 400px;
    border: 1px solid #ebeef5;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    text-align: left;
    overflow-y: auto;
    max-height: 200px;
    transition: all 0.3s ease;
}

.text {
    white-space: pre-wrap; /* 保持换行符 */
    font-size: 16px;
    color: #333;
    line-height: 1.5;
    word-break: break-word; /* 确保单词在容器边界换行 */
}

p {
    text-align: justify;
    margin: 0;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 8px; /* 设置滚动条的宽度 */
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: #c1c1c1; /* 滚动条的滑块颜色 */
    border-radius: 10px; /* 滑块的圆角 */
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background-color: #a8a8a8; /* 滑块在鼠标悬停时的颜色 */
}

.custom-scrollbar::-webkit-scrollbar-track {
    background-color: #f1f1f1; /* 滚动条的轨道颜色 */
    border-radius: 10px; /* 轨道的圆角 */
}

.content-text {
    margin-bottom: 0 !important;
    cursor: pointer;
    position: relative;
    max-width: 500px;
    white-space: pre-wrap;
    overflow-wrap: break-word;
}

.content-text::after {
    content: '';
    position: absolute;
    left: 50%;
    bottom: -5px; /* 增加与文字的距离 */
    width: 0;
    height: 3px;
    background: linear-gradient(90deg, #00ffcc, #3399ff);
    transition: width 0.4s ease, left 0.4s ease;
    border-radius: 5px;
}

.content-text:hover::after {
    width: 100%;
    left: 0;
    animation: none;
}

.content-text.active::after {
    animation: pulse 0.6s ease forwards;
}

.dialog-recognition-container {
    margin-top: 10px;
    width: 500px;
}
</style>
