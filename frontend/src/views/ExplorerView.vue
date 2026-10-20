<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import PageTitle from '@/components/ui/PageTitle.vue'
import DocumentRow from '@/components/layout/DocumentRow.vue'
import {useFiltersStore} from '@/stores/filters'
import {useDocumentsStore} from '@/stores/documents'
import {usePreviewStore} from '@/stores/preview'
import {useDownload} from '@/composables/useDownload'
import Icon from "@/components/ui/Icon.vue";
import { useI18n } from 'vue-i18n'

const filters = useFiltersStore()
const docs = useDocumentsStore()
const preview = usePreviewStore()
const { downloadDocument } = useDownload()
const { t } = useI18n()

const sortBy = ref('recent')

onMounted(() => {
  if (!docs.items.length) docs.fetchAll({ page: 1, page_size: 20 })
})

const filteredDocuments = computed(() => {
  const query = filters.search.toLowerCase().trim()

  return docs.items.filter((item) => {
    const matchesQuery = !query || `${item.title} ${item.subject} ${item.author}`.toLowerCase().includes(query)
    const matchesSubject = filters.subjectFilter === 'all' || item.subject === filters.subjectFilter
    const matchesFormat = filters.formatFilter === 'all' || item.format.toUpperCase() === filters.formatFilter.toUpperCase()
    return matchesQuery && matchesSubject && matchesFormat
  })
})
</script>

<template>
  <PageTitle
      :eyebrow="t('explorer.eyebrow')"
      :title="t('explorer.title')"
      :subtitle="t('explorer.subtitle', { count: docs.total })"
  />

  <p v-if="docs.error" class="error-state">{{ docs.error }}</p>

  <div class="filters">
    <label class="search-field">
      <Icon icon="Search" :size="21" />
      <input v-model="filters.search" type="search" :placeholder="t('label.searchPlaceholder')" />
    </label>

    <select v-model="filters.subjectFilter" :aria-label="t('label.filterSubject')">
      <option value="all">{{ t('label.allSubjects') }}</option>
      <option>Algorithmique</option>
      <option>Mathématiques</option>
      <option>Informatique</option>
      <option>Économie</option>
      <option>Droit</option>
    </select>

    <select v-model="filters.formatFilter" :aria-label="t('label.filterFormat')">
      <option value="all">{{ t('label.allFormats') }}</option>
      <option>PDF</option>
      <option>DOCX</option>
      <option>PPTX</option>
    </select>
  </div>

  <div class="results-card">
    <div class="results-header">
      <span>{{ filteredDocuments.length }} {{ filteredDocuments.length > 1 ? t('explorer.foundMany') : t('explorer.foundOne') }}</span>
      <select v-model="sortBy" :aria-label="t('label.sort')">
        <option value="recent">{{ t('explorer.recent') }}</option>
        <option value="downloads">{{ t('explorer.downloads') }}</option>
      </select>
    </div>

    <DocumentRow
        v-for="document in filteredDocuments"
        :key="document.id"
        :document="document"
        @preview="preview.open"
        @download="downloadDocument"
    />

    <p v-if="docs.loading" class="empty-state">{{ t('explorer.loading') }}</p>
    <p v-else-if="!filteredDocuments.length" class="empty-state">{{ t('explorer.empty') }}</p>
  </div>
</template>

<style scoped>
.filters {
  display: grid;
  grid-template-columns:1fr 165px 128px;
  gap: 10px;
  margin-bottom: 15px
}

.search-field, .filters select, .form-label input, .form-label select, .form-label textarea {
  height: 47px;
  padding: 0 13px;
  border: 1px solid var(--line);
  border-radius: 9px;
  outline: 0;
  color: var(--ink);
  background: #fff;
  font-size: 12px
}

.search-field {
  display: flex;
  align-items: center;
  gap: 10px
}

.search-field span {
  font-size: 22px
}

.search-field input {
  width: 100%;
  border: 0;
  outline: 0
}

.filters select {
  width: 100%
}

.results-card {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 16px;
  overflow: hidden;
}

.results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 17px;
  color: var(--muted);
  font-size: 11px
}

.results-header select {
  border: 0;
  color: var(--muted);
  font-size: 11px
}

.empty-state {
  padding: 35px;
  text-align: center;
  color: var(--muted);
  font-size: 13px
}

@media (max-width: 720px) {
  .filters {
    grid-template-columns:1fr
  }

}


</style>