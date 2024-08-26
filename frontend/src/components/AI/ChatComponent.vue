<template>
    <div class="chat-container">
        <div class="header">
            <span>小 E</span>
            <div class="header-buttons">
                <el-button icon="el-icon-close" class="header-button" @click="closeChat" />
            </div>
        </div>
        <div class="messages" ref="messagesContainer">
            <div v-for="message in messages" :key="message.id" :class="['message', message.sender]">
                <p>{{ message.text }}</p>
            </div>
        </div>
        <div class="input-container">
            <el-input v-model="inputMessage" @keyup.enter="sendMessage" placeholder="Ask AI anything..." />
            <div class="send-button" @click="sendMessage">
                <div v-if="loading" class="loader"></div>
                <div v-else class="send-icon">&#9658;</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick, defineEmits } from 'vue'
import { useProfileStore } from '@/store/profile.ts'
import api from '@/api'

const inputMessage = ref('')
const messages = ref([])
const messagesContainer = ref(null)
const loading = ref(false)
const emit = defineEmits(['closeChat'])

const sendMessage = async () => {
    if (inputMessage.value.trim() === '') return

    const userMessage = {
        id: Date.now(),
        text: inputMessage.value,
        sender: 'user',
    }

    messages.value.push(userMessage)
    api.uploadAiChat(userMessage)
    loading.value = true

    try {
        const tem = inputMessage.value
        inputMessage.value = ''
        const response = await api.chat({
            content: tem,
        })
        const botMessage = {
            id: Date.now() + 1,
            text: response.data.response,
            sender: 'bot',
        }
        messages.value.push(botMessage)
        api.uploadAiChat(botMessage)
    } catch (error) {
        console.error('Error:', error)
    } finally {
        loading.value = false
    }

    nextTick(() => {
        scrollToBottom()
    })
}

const scrollToBottom = () => {
    if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
}

const profile = useProfileStore()

onMounted(async () => {
    messages.value = await api.queryAiChat({
        user_id: profile.id,
    })
    nextTick(() => {
        scrollToBottom()
    })
})

const closeChat = () => {
    emit('closeChat')
}
</script>

<style scoped>
.chat-container {
    display: flex;
    flex-direction: column;
    height: 600px;
    width: 400px;
    background: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    font-family: 'Arial', sans-serif;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
    background: #f5f5f5;
    border-bottom: 1px solid #ddd;
    font-weight: bold;
}

.header-buttons {
    display: flex;
    gap: 5px;
}

.header-button {
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: 20px;
    padding: 5px;
}

.messages {
    flex: 1;
    overflow-y: auto;
    padding: 15px;
    background: #fafafa;
    border-bottom: 1px solid #ddd;
}

.message {
    padding: 10px 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    max-width: 75%;
    word-wrap: break-word;
}

.message.user {
    align-self: flex-end;
    background-color: #e1f5fe;
    color: #0277bd;
}

.message.bot {
    align-self: flex-start;
    background-color: #eeeeee;
    color: #333;
}

.input-container {
    display: flex;
    align-items: center;
    padding: 10px;
    background: #fff;
}

.el-input {
    flex: 1;
    border-radius: 20px;
    background: #f5f5f5;
    border: 1px solid #ddd;
}

.el-input input {
    background: none;
    border: none;
    outline: none;
}

.send-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #007bff;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.3s ease;
    margin-left: 10px;
}

.send-button:hover {
    background: #0056b3;
}

.send-icon {
    color: #fff;
    font-size: 20px;
}

.loader {
    border: 2px solid #f3f3f3;
    border-top: 2px solid #fff;
    border-radius: 50%;
    width: 16px;
    height: 16px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}
</style>
