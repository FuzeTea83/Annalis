import type { DocumentItem } from '@/types/document'
import {documentsApi} from "@/api/documents.ts";

export function useDownload() {
    async function downloadDocument(doc: DocumentItem) {
        try {
            const url = await documentsApi.download(doc.id)
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
