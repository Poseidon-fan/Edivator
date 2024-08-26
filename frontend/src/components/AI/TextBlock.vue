<template>
    <div class="custom-text-block">
        {{ content }}
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps({
    content: {
        type: String,
    },
})
</script>

<style scoped>
.custom-text-block {
    border: 1px solid #e0e0e0; /* 浅灰色边框 */
    background-color: #f9f9f9; /* 浅色背景 */
    border-radius: 4px; /* 圆角边框 */
    padding: 8px; /* 内部填充 */
    margin: 4px 0; /* 外部间距 */
    font-family: 'Arial', sans-serif; /* 字体 */
    color: #333; /* 文本颜色 */
}
</style>
