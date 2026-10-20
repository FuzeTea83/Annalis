import {defineStore} from 'pinia'
import {ref} from 'vue'
import type {DocumentItem} from '@/types/document'
import {documentsApi} from "@/api/documents.ts";
import {ApiError} from "@/api/http.ts";

export const usePreviewStore = defineStore('preview', () => {
    const document = ref<DocumentItem | null>(null)
    const url = ref<string | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    function revoke() {
        if (url.value?.startsWith('blob:')) {
            URL.revokeObjectURL(url.value)
        }
        url.value = null
    }

    async function fetchContent() {
        const id = document.value?.id
        if (!id) {
            error.value = 'Aucun document sélectionné'
            return
        }

        loading.value = true
        error.value = null
        revoke()

        try {
            url.value = await documentsApi.preview(id)
        } catch (e) {
            error.value = e instanceof ApiError ? e.message : "Erreur réseau"
            document.value = null
        } finally {
            loading.value = false
        }
    }

    async function open(doc: DocumentItem) {
        document.value = doc
        await fetchContent()
    }

    function close() {
        revoke()
        document.value = null
    }

    return { document, url, loading, error, open, close, fetchContent }
})