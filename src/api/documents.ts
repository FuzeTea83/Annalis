import {api} from '@/api/http'
import type {DocumentItem} from '@/types/document'

export const documentsApi = {
    list: (params: { q?: string; subject?: string; format?: string; page?: number; page_size?: number } = {}) => {
        const query = new URLSearchParams(
            Object.entries(params).filter(([, v]) => v !== undefined && v !== '') as [string, string][],
        )
        return api.get<{ data: DocumentItem[]; total: number }>(`/documents/view?${query}`)
    },

    upload: (formData: FormData): Promise<DocumentItem> => {
        return api.post<DocumentItem>('/documents/upload', formData)
    },

    download: async (id: string): Promise<string> => {
        const blob = await api.get<Blob>(`/documents/${id}/download`, {responseType: 'blob'})
        return URL.createObjectURL(blob)
    },

    recent: () => api.get<{ data: DocumentItem[]; total: number }>(`/documents/recent`),

    owned: () => api.get<{ data: DocumentItem[]; total: number }>(`/documents/owned`),

    preview: async (id: string): Promise<string> => {
        const blob = await api.get<Blob>(`/documents/${id}/preview`, {responseType: 'blob'})
        return URL.createObjectURL(blob)
    },
}
