import { api } from '@/api/http'
import type { DocumentItem } from '@/types/document'

export const documentsApi = {
    list: (params: { q?: string; subject?: string; format?: string; page?: number } = {}) => {
        const query = new URLSearchParams(
            Object.entries(params).filter(([, v]) => v !== undefined && v !== '') as [string, string][],
        )
        return api.get<{ data: DocumentItem[]; total: number }>(`/documents?${query}`)
    },

    upload: (formData: FormData): Promise<DocumentItem> => {
        return api.post<DocumentItem>(`/documents`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    },

    downloadUrl: (id: string) => `${import.meta.env.VITE_API_URL ?? '/api'}/documents/${id}/file`,
}
