import { defineStore } from 'pinia'
import { h, ref, type Component } from 'vue'

export const mainStore = defineStore('main', {
    state: () => {
        return {
            helloPinia: '你好 Pinia!',
        }
    },
    getters: {},
    actions: {},
    persist: true,
})

export const useEditorStore = defineStore('editor', () => {
    const headings = ref()
    const activeHeading = ref()
    const editorInstance = ref()
    
    const setHeadings = (data) => {
        headings.value = data
    }
    const setActiveHeading = (data) => {
        activeHeading.value = data
    }
    const setEditorInstance = (data) => {
        console.log(editorInstance.value)
        editorInstance.value = data
    }
    
    return {
        headings,
        setHeadings,
        activeHeading,
        setActiveHeading,
        editorInstance,
        setEditorInstance,
    }
}, {
    persist: {
        key: 'editor-store',
        storage: window.sessionStorage,
        paths: ['headings', 'activeHeading'],
    }
})
