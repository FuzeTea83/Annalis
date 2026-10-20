<script setup lang="ts">
import {computed} from 'vue'
import DocumentPreviewModal from '@/components/DocumentPreviewModal.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import Topbar from '@/components/Topbar.vue'
import type {NavItem} from './types/views'
import {useRoute} from 'vue-router'
import {usePreviewStore} from "@/stores/preview.ts";
import {useDownload} from '@/composables/useDownload'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const preview = usePreviewStore()
const {downloadDocument} = useDownload()
const { t } = useI18n()

const navItems = computed<NavItem[]>(() => [
  {id: 'overview', label: t('sidebar.overview'), icon: 'House'},
  {id: 'explorer', label: t('sidebar.explorer'), icon: 'Book'},
  {id: 'upload', label: t('sidebar.upload'), icon: 'Upload'},
])

const currentTitle = computed(() => {
  const titles: Record<string, string> = {
    overview: t('home.recent'),
    explorer: t('explorer.title'),
    upload: t('upload.title'),
    account: t('account.title'),
  }
  return titles[String(route.name)] ?? 'Annalis'
})
const isAuthPage = computed(() => route.meta.hideNavigation || route.name === 'login' || route.name === 'sign-up')
</script>

<template>
  <template v-if="isAuthPage">
    <router-view/>
  </template>
  <div v-else class="app-shell">
    <Sidebar :nav-items="navItems"/>
    <main class="main-content">
      <Topbar :title="currentTitle" @open-account="$router.push({ name: 'account' })"/>
      <div class="content">
        <router-view/>
      </div>
    </main>
    <DocumentPreviewModal
        v-if="preview.document && preview.url"
        :document="preview.document"
        :url="preview.url"
        @close="preview.close()"
        @download="downloadDocument"
    />
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  min-height: 100vh;
  background: #fbfcfa
}

.main-content {
  min-width: 0;
  flex: 1
}

.content {
  max-width: 1120px;
  margin: 0 auto;
  padding: 68px 64px 96px
}

@media (max-width: 1000px) {
  .content {
    padding-inline: 32px
  }
}


@media (max-width: 720px) {
  .content {
    padding: 42px 20px 64px
  }
}
</style>