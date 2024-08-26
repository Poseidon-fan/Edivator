<template>
    <div class="ai-writer">
        <div class="input-container">
            <textarea
                class="prompt-textarea"
                v-model="content"
                placeholder="Tell me what you want me to write about."
                @click="onClickTextArea"
                @input.prevent.stop="handleInput"
                @keydown="handleKeyDown"
                @focus="onFocus"
                @blur="onBlur"
                ref="textArea"
                @input="adjustHeight"
            ></textarea>
            <el-button class="send-button" type="primary" @click="generateText">
                <i class="el-icon-s-promotion"></i>
            </el-button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, nextTick, defineProps } from 'vue'
import { ElMessage } from 'element-plus'
import { useEditorUpdateStore } from '@/store/editorUpdate'

// 接收 props
const props = defineProps({
    onUpdate: Function,
    content: String,
})

const content = ref('')
const editorUpdateStore = useEditorUpdateStore()
const textArea = ref(null)
const onClickTextArea = () => {
    setTimeout(() => {
        textArea.value.focus()
        editorUpdateStore.editorUpdateInProgress = true
    }, 50)
}
const changeTone = () => {
    setTimeout(() => {
        textArea.value.focus()
        editorUpdateStore.editorUpdateInProgress = true
    }, 50)
    ElMessage.info('Change tone clicked')
}

const generateText = () => {
    ElMessage.success('Generate text clicked')
}

// 监听 content 的变化
watch(content, (newValue) => {
    if (!editorUpdateStore.editorUpdateInProgress) {
        props.onUpdate(newValue)
    }
})

const onFocus = () => {
    editorUpdateStore.editorUpdateInProgress = true
    textArea.value.classList.add('focused')
}

const onBlur = () => {
    editorUpdateStore.editorUpdateInProgress = false
    textArea.value.classList.remove('focused')
}

const handleInput = (e) => {
    content.value = (event.target as HTMLTextAreaElement).value
}

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === 'Enter') {
        if (event.shiftKey) {
            // Shift+Enter 换行
            const start = textArea.value.selectionStart
            const end = textArea.value.selectionEnd
            content.value = content.value.substring(0, start) + '\n' + content.value.substring(end)
            nextTick(() => {
                textArea.value.selectionStart = textArea.value.selectionEnd = start + 1
            })
        } else {
            // Enter 发送
            event.preventDefault()
            generateText()
        }
    }
}

const adjustHeight = () => {
    textArea.value.style.height = 'auto'
    textArea.value.style.height = `${textArea.value.scrollHeight}px`
}

// 让文本区域获取焦点
onMounted(() => {
    if (textArea.value) {
        setTimeout(() => {
            textArea.value.focus()
            editorUpdateStore.editorUpdateInProgress = true
        }, 50)
        adjustHeight()
    }
})
</script>

<style scoped>
@keyframes borderPulse {
    0% {
        box-shadow: 0 0 5px #0ff, 0 0 10px #0ff, 0 0 15px #0ff, 0 0 20px #0ff;
    }
    50% {
        box-shadow: 0 0 10px #0ff, 0 0 20px #0ff, 0 0 30px #0ff, 0 0 40px #0ff;
    }
    100% {
        box-shadow: 0 0 5px #0ff, 0 0 10px #0ff, 0 0 15px #0ff, 0 0 20px #0ff;
    }
}

@keyframes buttonClick {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(0.95);
    }
    100% {
        transform: scale(1);
    }
}

.ai-writer {
    width: 600px;
    margin: auto;
}

.input-container {
    display: flex;
    background: #34495e;
    border-radius: 20px;
    border: 1px solid #1abc9c;
    padding: 10px;
    transition: border-color 0.3s ease;
}

.prompt-textarea {
    flex-grow: 1;
    border: none;
    outline: none;
    font-size: 16px;
    resize: none;
    min-height: 60px;
    padding: 10px;
    border-radius: 30px;
    background: transparent;
    color: #ecf0f1;
    transition: box-shadow 0.3s ease;
}

.prompt-textarea.focused {
    animation: borderPulse 1.5s infinite;
}

.prompt-textarea::placeholder {
    color: #95a5a6;
}

.send-button {
    margin-left: 10px;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(145deg, #1abc9c, #16a085);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    animation: buttonClick 0.3s ease;
}

.send-button:active {
    animation: buttonClick 0.3s ease;
}

.el-icon-s-promotion {
    font-size: 20px;
    color: #fff;
}
</style>
