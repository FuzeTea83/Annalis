<script setup lang="ts">
import {computed, onMounted} from 'vue'
import type {DocumentItem, RecentDocumentItem} from '@/types/document'
import PageTitle from '@/components/PageTitle.vue'
import DocumentRow from '@/components/layout/DocumentRow.vue'
import {useAuthStore} from '@/stores/auth'
import {useDocumentsStore} from '@/stores/documents'
import {usePreviewStore} from "@/stores/preview.ts";
import {useDownload} from "@/composables/useDownload.ts";
import AnnalisButton from "@/components/ui/AnnalisButton.vue";
import {useI18n} from "vue-i18n";

const {t, d,} = useI18n()
const auth = useAuthStore()
const docsStore = useDocumentsStore()
const preview = usePreviewStore()
const {downloadDocument} = useDownload()

onMounted(() => {
  docsStore.fetchRecent()
})

const firstName = computed(() => {
  if (auth.user?.firstName) return auth.user.firstName
  return ''
})

const recentDocs = computed(() => {
  return docsStore.items.filter((doc): doc is RecentDocumentItem => 'viewedAt' in doc && doc.viewedAt != null).sort((a, b) => {
    if (!a.viewedAt || !b.viewedAt) return 0
    return new Date(b.viewedAt).getTime() - new Date(a.viewedAt).getTime()
  })
})

const formattedDate = computed(() => {
  const text = d(new Date(), 'short');
  return text
      .split(" ")
      .map((word) => (word ? word.charAt(0).toUpperCase() + word.slice(1) : word))
      .join(" ");
})

</script>

<template>
  <div class="home-container">
    <div class="home-topbar-row">
      <PageTitle
          :eyebrow="formattedDate"
          :title="`Bonjour ${firstName},`"
          subtitle="Prête à avancer dans tes cours aujourd'hui ?"
      />
      <router-link to="/upload">
        <AnnalisButton :label="t('home.upload_document')" variant="primary" :icon="{ icon: 'Upload', leading: true }"/>
      </router-link>
    </div>

    <section class="recent-documents-panel">
      <div class="panel-header">
        <div>
          <p class="eyebrow">REPRENDRE</p>
          <h2 class="panel-title">Consultés récemment</h2>
        </div>
        <router-link to="/explorer" class="text-link">Tout voir <span>→</span></router-link>
      </div>

      <div class="recent-documents-list">
        <DocumentRow
            v-for="document in recentDocs"
            :key="document.id"
            :document="document"
            variant="recent"
            @preview="preview.open"
            @download="downloadDocument"
        />
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.home-topbar-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.recent-documents-panel {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 16px;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px 28px 16px;
}

.panel-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--ink);
  margin-top: 4px;
}

.recent-documents-list {
  display: flex;
  flex-direction: column;
}
</style>

