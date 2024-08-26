<template>
    <div class="dialog">
        <button @click="copyContent" class="copy-button">
            <img src="@/assets/copy-icon.png" alt="复制" class="copy-icon" />
            复制
        </button>
        <div class="dialog-content">
            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
            </div>
            <div v-else class="text-container">
                <div v-html="currentContent"></div>
            </div>
        </div>
        <div class="dialog-footer">
            <button @click="closeDialog" class="close-button">关闭</button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue'

const props = defineProps({
    fullContent: String,
    loading: Boolean,
})

const emit = defineEmits(['close'])

const currentContent = ref('')
let timer: number | null = null

watch(props, (newProps) => {
    if (!newProps.loading && newProps.fullContent) {
        renderText(newProps.fullContent)
    }
})

const renderText = (text: string) => {
    currentContent.value = ''
    let index = 0
    timer = setInterval(() => {
        if (index < text.length) {
            currentContent.value += text[index]
            index++
        } else {
            clearInterval(timer!)
            timer = null
        }
    }, 50)
}

const closeDialog = () => {
    emit('close')
}

const copyContent = () => {
    navigator.clipboard
        .writeText(props.fullContent)
        .then(() => {
            alert('内容已复制到剪贴板')
        })
        .catch((err) => {
            console.error('复制失败', err)
        })
}
</script>

<style scoped>
.dialog {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #e3f2fd; /* Light blue background color */
    border: 1px solid #90caf9; /* Light blue border color */
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    width: 500px;
    max-width: 100%;
    padding: 10px;
    display: flex;
    flex-direction: column;
    font-family: 'Arial', sans-serif;
    animation: border-animation 2s infinite;
}

@keyframes border-animation {
    0% {
        box-shadow: 0 0 6px 1px #90caf9;
    }
    50% {
        box-shadow: 0 0 12px 2px #42a5f5;
    }
    100% {
        box-shadow: 0 0 6px 1px #90caf9;
    }
}

.copy-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: transparent;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    font-size: 14px;
    color: #007bff;
}

.copy-button:hover {
    color: #0056b3;
}

.copy-icon {
    width: 16px;
    height: 16px;
    margin-right: 5px;
}

.dialog-content {
    flex: 1;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 20px;
    width: 100%;
    color: #333;
    min-height: 100px;
    max-height: 200px;
    overflow: auto;
}

.loading-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}

.text-container {
    width: 100%;
    text-align: left;
    padding: 10px;
    background-color: #ffffff; /* White background for text container */
    border-radius: 5px;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
    margin-top: 5px;
}

.close-button {
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
    font-size: 14px;
    padding: 5px 10px;
    border-radius: 5px;
    transition: background-color 0.3s;
}

.close-button:hover {
    background-color: #0056b3;
}

.loading-spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-top: 4px solid #007bff;
    border-radius: 50%;
    width: 30px;
    height: 30px;
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
