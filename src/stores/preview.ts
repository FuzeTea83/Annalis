import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { DocumentItem } from '@/types/document'

export const usePreviewStore = defineStore('preview', () => {
    const document = ref<DocumentItem | null>(null)

    function open(doc: DocumentItem) {
        document.value = doc
    }

    function close() {
        document.value = null
    }

    return { document, open, close }
})