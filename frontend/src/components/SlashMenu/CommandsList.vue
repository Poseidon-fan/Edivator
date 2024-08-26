<template>
    <div class="command-popup" @keydown="onKeyDown" tabindex="0">
        <div id="scrollingDiv" class="command-list">
            <button
                class="command-item"
                :class="{ active: index === selectedIndex }"
                v-for="(item, index) in items"
                :key="index"
                @click="selectItem(index)"
            >
                <div class="icon-container">
                    <Icon :icon="item.icon" />
                </div>
                <span class="item-title">{{ item.title }}</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import Icon from './Icon.vue'
import type { PropType } from 'vue'

const props = defineProps<{
    items: { icon: string; title: string }[]
    command: (item: any) => void
}>()

const selectedIndex = ref(0)
const scrollingDiv = ref<HTMLElement | null>(null)

onMounted(() => {
    scrollingDiv.value = document.getElementById('scrollingDiv') as HTMLElement
    document.querySelector('.command-popup')?.focus()
})

watch(
    () => props.items,
    () => {
        selectedIndex.value = 0
    }
)

const onKeyDown = (event: KeyboardEvent) => {
    if (event.key === 'ArrowUp') {
        upHandler()
        event.preventDefault()
    }
    if (event.key === 'ArrowDown') {
        downHandler()
        event.preventDefault()
    }
    if (event.key === 'Enter') {
        enterHandler()
        event.preventDefault()
    }
}

const upHandler = () => {
    selectedIndex.value = (selectedIndex.value + props.items.length - 1) % props.items.length
    scrollDiv()
}

const downHandler = () => {
    selectedIndex.value = (selectedIndex.value + 1) % props.items.length
    scrollDiv()
}

const scrollDiv = () => {
    if (scrollingDiv.value) {
        const buttons = scrollingDiv.value.querySelectorAll('button')
        const button = buttons[selectedIndex.value]
        button.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'start',
        })
    }
}

const enterHandler = () => {
    selectItem(selectedIndex.value)
}

const selectItem = (index: number) => {
    const item = props.items[index]
    if (item) {
        props.command(item)
    }
}
</script>

<style scoped>
.command-popup {
    width: 10vw;
    max-width: 160px;
    background: linear-gradient(135deg, #1f1f1f 0%, #3d3d3d 100%);
    border: 1px solid #2e2e2e;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    overflow: hidden;
    outline: none; /* To enable focus outline */
}

.command-list {
    max-height: 52vh;
    overflow-y: auto;
    padding: 8px;
}

.command-item {
    display: flex;
    align-items: center;
    padding: 6px 10px;
    font-size: 0.85rem;
    color: #e0e0e0;
    background: transparent;
    border: none;
    outline: none;
    cursor: pointer;
    transition: background 0.3s, transform 0.3s;
}

.command-item:hover {
    background: #4a4a4a;
    transform: scale(1.05);
}

.command-item.active {
    background: #4a4a4a;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.2);
}

.icon-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    margin-right: 6px;
    background: #2a2a2a;
    border-radius: 4px;
    transition: background 0.3s;
}

.icon-container:hover {
    background: #1a1a1a;
}

.item-title {
    flex-grow: 1;
}
</style>
