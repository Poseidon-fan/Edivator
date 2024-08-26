<template>
    <div>
        <el-button class="chat-button" @click="showChat = true">
            <img src="@/assets/images/chat-icon.png" alt="Chat Icon" />
        </el-button>

        <div v-if="showChat" class="modal-overlay" @click.self="closeChat">
            <div class="modal-content">
                <ChatComponent @closeChat="closeChat" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import ChatComponent from '@/components/AI/ChatComponent.vue'

const showChat = ref(false)

const closeChat = () => {
    showChat.value = false
}
</script>

<style scoped>
.chat-button {
    position: fixed;
    bottom: 100px;
    right: 20px;
    background-color: transparent;
    border: none;
    padding: 0;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    border-radius: 50%;
    transition: transform 0.3s ease;
    z-index: 1000;
}

.chat-button:hover {
    transform: scale(1.1);
}

.chat-button img {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    transition: box-shadow 0.3s ease;
}

.chat-button img:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    width: 400px;
    max-width: 90%;
    overflow: hidden;
    z-index: 1001;
}
</style>
