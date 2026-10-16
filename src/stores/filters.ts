import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useFiltersStore = defineStore('filters', () => {
    const search = ref('')
    const subjectFilter = ref('Toutes les matières')
    const formatFilter = ref('Tous les formats')
    return { search, subjectFilter, formatFilter }
})