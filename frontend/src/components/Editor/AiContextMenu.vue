<template>
    <ul
        v-show="visiblemenu"
        :style="{
            left: `${position.left}px`,
            top: `${position.top}px`,
            display: visiblemenu ? 'flex' : 'none',
        }"
        class="contextmenu"
        @mousedown.stop
    >
        <li class="item" @mouseenter="showAiMenu = true" @mouseleave="showAiMenu = false">
            <img src="@/assets/ai.png" alt="AI" class="icon-img" />
            <ul v-show="showAiMenu" class="submenu">
                <li class="subitem" @click="abstract">摘要</li>
                <li class="subitem" @click="polish">修饰</li>
                <li class="subitem" @click="translate">翻译</li>
                <li class="subitem" @click="correct">改错</li>
                <li class="subitem" @click="continuation">续写</li>
            </ul>
        </li>
        <li class="item">待定</li>
        <li class="item">待定</li>
        <li class="item">待定</li>
        <li class="item">待定</li>
    </ul>
    <Dialog
        v-if="dialogVisible"
        :fullContent="fullDialogContent"
        :loading="dialogLoading"
        @close="dialogVisible = false"
    />
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'
import api from '@/api'
import Dialog from './Dialog.vue'

const props = defineProps({
    visiblemenu: Boolean,
    position: Object,
    content: String,
})

const emit = defineEmits(['closeMenu', 'updateDialog'])

const showAiMenu = ref(false)
const dialogVisible = ref(false)
const dialogLoading = ref(false)
const fullDialogContent = ref('')

const showLoadingDialog = () => {
    dialogVisible.value = true
    dialogLoading.value = true
    fullDialogContent.value = ''
}

const updateDialogContent = (newContent: string) => {
    dialogLoading.value = false
    fullDialogContent.value = newContent
}

const abstract = async () => {
    showLoadingDialog()
    const ret = await api.abstract({
        content: props.content,
    })
    updateDialogContent(ret)
}

const polish = async () => {
    showLoadingDialog()
    const ret = await api.polish({
        content: props.content,
    })
    updateDialogContent(ret)
}

const translate = async () => {
    showLoadingDialog()
    const ret = await api.translate({
        content: props.content,
        language: 'en',
    })
    updateDialogContent(ret)
}

const correct = async () => {
    showLoadingDialog()
    const ret = await api.correct({
        content: props.content,
    })
    updateDialogContent(ret)
}

const continuation = async () => {
    showLoadingDialog()
    const ret = await api.continueWrite({
        content: props.content,
    })
    updateDialogContent(ret)
}
</script>

<style scoped>
.contextmenu {
    position: absolute;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
    z-index: 1000;
    padding: 10px;
    list-style: none;
    display: flex;
    justify-content: space-around;
    align-items: center;
    width: 300px;
}

.item {
    padding: 10px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    min-width: 50px;
    position: relative;
}

.item:first-child:hover {
    background-color: rgba(0, 0, 0, 0) !important;
}

.item:hover {
    background-color: #f0f0f0;
    border-radius: 3px;
}

.icon-img {
    width: 50px;
    height: 50px;
}

.submenu {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
    list-style: none;
    padding: 10px;
    display: flex;
    flex-direction: column;
    white-space: nowrap;
}

.subitem {
    padding: 10px;
    cursor: pointer;
    display: flex;
    align-items: center;
    text-align: center;
}

.subitem:hover {
    background-color: #f0f0f0;
    border-radius: 3px;
}

.icon {
    margin-right: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
