import type { DocumentItem } from '@/types/document'

const BASE = import.meta.env.VITE_API_URL ?? '/api'

export function useDownload() {
    async function downloadDocument(doc: DocumentItem) {
        try {
            const response = await fetch(`${BASE}/documents/${doc.id}/download`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token') ?? ''}` },
            })
            if (!response.ok) throw new Error('Téléchargement impossible')
            const blob = await response.blob()
            const url = URL.createObjectURL(blob)
            const link = globalThis.document.createElement('a')
            link.href = url
            link.download = `${doc.title.replaceAll(' ', '-').toLowerCase()}.${doc.format.toLowerCase()}`
            link.click()
            URL.revokeObjectURL(url)
        } catch {
            window.alert('Le téléchargement a échoué. Réessaie dans un instant.')
        }
    }

    return { downloadDocument }
}
