<template>
    <button
        class="menu-item"
        :class="{ 'is-active': props.isActive ? props.isActive() : null }"
        @click="props.action"
        :title="props.title"
    >
        <svg class="remix">
            <use :xlink:href="`${remixiconUrl}#ri-${props.icon}`" />
        </svg>
    </button>
</template>

<script setup lang="ts">
import remixiconUrl from 'remixicon/fonts/remixicon.symbol.svg'

const props = defineProps<{
    icon: string
    title: string
    action: Function
    isActive?: Function
}>()
</script>

<style>
.menu-item {
    background: transparent;
    border: none;
    border-radius: 0.4rem;
    color: #333;
    cursor: pointer;
    height: 1.75rem;
    padding: 0.25rem;
    margin-right: 0.25rem;
    width: 1.75rem;
}

.menu-item svg {
    fill: currentColor;
    height: 100%;
    width: 100%;
}

.menu-item.is-active,
.menu-item:hover {
    background-color: #d6d6d6;
}
</style>
