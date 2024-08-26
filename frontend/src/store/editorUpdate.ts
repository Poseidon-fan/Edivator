// src/store/editorUpdate.js

import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useEditorUpdateStore = defineStore('editorUpdate', () => {
    const editorUpdateInProgress = ref(false)

    return {
        editorUpdateInProgress,
    }
}, {
    persist: {
        key: 'editor-update-store',
        storage: window.sessionStorage,
        paths: ['editorUpdateInProgress'],
    }
})
