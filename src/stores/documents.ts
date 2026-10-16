import {defineStore} from "pinia";
import {ref} from "vue";
import type {DocumentItem} from "@/types/document.ts";
import {documentsApi} from "@/api/documents.ts";
import {ApiError} from "@/api/http.ts";
import {documents as initialDocuments} from "@/data/documents";

export const useDocumentsStore = defineStore('documents', () => {
    const items = ref<DocumentItem[]>([...initialDocuments])
    const total = ref(initialDocuments.length)
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function fetchAll(params?: Parameters<typeof documentsApi.list>[0]) {
        loading.value = true
        error.value = null
        try {
            const res = await documentsApi.list(params)
            if (res && Array.isArray(res.data)) {
                items.value = res.data
                total.value = res.total ?? res.data.length
            }
        } catch (e) {
            error.value = e instanceof ApiError ? e.message : null
            if (!items.value.length) {
                items.value = [...initialDocuments]
                total.value = initialDocuments.length
            }
        } finally {
            loading.value = false
        }
    }

    function addDocument(doc: DocumentItem) {
        items.value.unshift(doc)
        total.value = items.value.length
    }

    return { items, total, loading, error, fetchAll, addDocument }
})