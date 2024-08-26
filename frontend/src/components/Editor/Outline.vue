<template>
    <div class="outline__list">
        <h2 class="outline__title">TABLE OF CONTENTS</h2>
        <template v-for="(heading, index) in headings" :key="index">
            <el-popover trigger="click" placement="right">
                <template #reference>
                    <el-button
                        @click="handleHeadingClick(heading.start)"
                        text
                        class="outline__item"
                        :class="`outline__item--${heading.level}`"
                    >
                        {{ heading.text }}
                        <el-icon v-if="heading.icon">
                            <component :is="heading.icon" />
                        </el-icon>
                    </el-button>
                </template>
                <!-- 如果需要弹出内容，请在这里添加 -->
            </el-popover>
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useEditorStore } from '@/store'
import { storeToRefs } from 'pinia'
import { TextSelection } from 'prosemirror-state'

const editorStore = useEditorStore()
const { headings } = storeToRefs(editorStore)

const handleHeadingClick = (pos: number) => {
    const editor = editorStore.editor
    if (editor) {
        editor.view.dispatch(editor.state.tr.setSelection(TextSelection.create(editor.state.doc, pos)).scrollIntoView())
    }
}
</script>

<style scoped>
.outline__list {
    display: flex;
    flex-direction: column;
    padding: 1rem;
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    height: 100%;
}

.outline__title {
    color: #333;
    font-size: 18px;
    border-bottom: 1px solid #eee;
    padding-bottom: 0.5rem;
    text-align: left;
}

.outline__item {
    font-size: 14px;
    color: #333 !important;
    transition: color 0.3s, transform 0.3s;
    padding: 0.5rem 0;
    text-align: left;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

:deep(.el-button > span) {
    color: #666;
}

.outline__item:hover {
    color: #409eff;
    transform: translateX(5px);
}

.outline__item--1 {
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5rem !important;
}

.outline__item--2 {
    font-size: 14px;
    padding-left: 1rem !important;
}

.outline__item--3 {
    font-size: 13px;
    padding-left: 1.5rem !important;
}

.outline__item--4 {
    font-size: 12px;
    padding-left: 2rem !important;
}

.el-button {
    padding: 0;
    height: auto;
    line-height: 1.5;
    padding: 5px 0;
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.el-button + .el-button {
    margin-left: 0;
}

.el-icon {
    margin-left: 0.5rem;
}
</style>
