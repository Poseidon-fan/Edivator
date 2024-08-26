<template>
    <div class="ai-image">
        <div class="input-container">
            <textarea
                class="prompt-textarea"
                v-model="content"
                placeholder="Describe the image that you want me to generate."
                @click="onClickTextArea"
                @input.prevent.stop="handleInput"
                @keydown="handleKeyDown"
                @focus="onFocus"
                @blur="onBlur"
                ref="textArea"
                @input="adjustHeight"
            ></textarea>
            <el-button
                class="send-button"
                type="primary"
                @click="generateImage"
            >
                <i class="el-icon-picture"></i>
            </el-button>
            <el-dropdown class="dropdown" @command="changeStyle">
                <span class="el-dropdown-link">
                    {{ style }}
                    <i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu>
                    <el-dropdown-item
                        v-for="styleOption in styles"
                        :key="styleOption"
                        :command="styleOption"
                    >
                        {{ styleOption }}
                    </el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'

// 接收 props
const props = defineProps({
    onUpdate: Function,
    content: String,
})

const content = ref('')
const style = ref('二次元')
const styles = ref([
    '二次元',
    '写实风格',
    '古风',
    '赛博朋克',
    '水彩画',
    '油画',
    '卡通画',
])

const textArea = ref(null)
const onClickTextArea = () => {
    setTimeout(() => {
        textArea.value.focus()
    }, 50)
}

const changeStyle = (newStyle: string) => {
    style.value = newStyle
    ElMessage.info(`Change style to ${newStyle}`)
}

const generateImage = async () => {
    ElMessage.success(`Generating image with style: ${style.value}`)
    // 调用生成图像的API或相关逻辑
}

// 监听 content 的变化
watch(content, (newValue) => {
    props.onUpdate(newValue)
})

const onFocus = () => {
    textArea.value.classList.add('focused')
}

const onBlur = () => {
    textArea.value.classList.remove('focused')
}

const handleInput = (e) => {
    content.value = (e.target as HTMLTextAreaElement).value
}

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === 'Enter') {
        if (event.shiftKey) {
            // Shift+Enter 换行
            const start = textArea.value.selectionStart
            const end = textArea.value.selectionEnd
            content.value =
                content.value.substring(0, start) +
                '\n' +
                content.value.substring(end)
            nextTick(() => {
                textArea.value.selectionStart = textArea.value.selectionEnd =
                    start + 1
            })
        } else {
            // Enter 发送
            event.preventDefault()
            generateImage()
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

.ai-image {
    width: 600px;
    margin: auto;
    background: #34495e;
    border-radius: 20px;
    border: 1px solid #1abc9c;
    padding: 10px;
}

.input-container {
    display: flex;
    align-items: center;
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

.el-icon-picture {
    font-size: 20px;
    color: #fff;
}

.dropdown {
    margin-left: 10px;
}
</style>
