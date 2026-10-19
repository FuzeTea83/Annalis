import {defineStore} from "pinia";
import {ref} from "vue";
import type {DocumentItem} from "@/types/document.ts";
import {documentsApi} from "@/api/documents.ts";
import {ApiError} from "@/api/http.ts";

export const useDocumentsStore = defineStore('documents', () => {
    const items = ref<DocumentItem[]>([])
    const total = ref(0)
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function fetchAll(params?: Parameters<typeof documentsApi.list>[0]) {
        loading.value = true
        error.value = null
        try {
            const { data, total } = await documentsApi.list(params)
            if (data && Array.isArray(data)) {
                for (const doc of data) {
                    addDocument(doc)
                }
            }
        } catch (e) {
            error.value = e instanceof ApiError ? e.message : null
            if (!items.value.length) {
                items.value = []
                total.value = 0
            }
        } finally {
            loading.value = false
        }
    }

    function addDocument(doc: DocumentItem) {
        if (items.value.find(d => d.id === doc.id)) {
            return
        }
        items.value.unshift(doc)
        total.value = items.value.length
        doc.createdAt = new Date(doc.createdAt)
    }

    async function fetchRecent() {
        loading.value = true
        error.value = null
        try {
            const { data, total } = await documentsApi.recent()
            if (total !== 0 && Array.isArray(data)) {
                for (const doc of data) {
                    addDocument(doc)
                }
            }
        } catch (e) {
            error.value = e instanceof ApiError ? e.message : null
        } finally {
            loading.value = false
        }
    }

    async function fetchOwned() {
        loading.value = true
        error.value = null
        try {
            const { data, total } = await documentsApi.owned()
            if (total !== 0 && Array.isArray(data)) {
                for (const doc of data) {
                    addDocument(doc)
                }
            }
        } catch (e) {
            error.value = e instanceof ApiError ? e.message : null
        } finally {
            loading.value = false
        }
    }

    return { items, total, loading, error, fetchAll, addDocument, fetchRecent, fetchOwned}
})