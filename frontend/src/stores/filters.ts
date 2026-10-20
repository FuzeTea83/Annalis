import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useFiltersStore = defineStore('filters', () => {
    const search = ref('')
    const subjectFilter = ref('all')
    const formatFilter = ref('all')
    return { search, subjectFilter, formatFilter }
})