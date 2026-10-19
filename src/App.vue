<script setup lang="ts">
import {computed} from 'vue'
import DocumentPreviewModal from '@/components/DocumentPreviewModal.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import Topbar from '@/components/Topbar.vue'
import type {NavItem} from './types/views'
import {useRoute} from 'vue-router'
import {usePreviewStore} from "@/stores/preview.ts";
import {useDownload} from '@/composables/useDownload'

const route = useRoute()
const preview = usePreviewStore()
const {downloadDocument} = useDownload()

const navItems: NavItem[] = [
  {id: 'overview', label: 'Vue d’ensemble', icon: 'House'},
  {id: 'explorer', label: 'Explorer', icon: 'Book'},
  {id: 'upload', label: 'Déposer un document', icon: 'Upload'},
]

const currentTitle = computed(() => (route.meta.title as string) ?? 'Annalis')
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