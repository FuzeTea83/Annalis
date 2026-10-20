<script setup lang="ts">
import type {DocumentItem} from '@/types/document.ts'
import AnnalisButton from "@/components/ui/AnnalisButton.vue";
import {computed} from "vue";
import {useI18n} from "vue-i18n";

const props = defineProps<{
  document: DocumentItem,
  url: string
}>()

const emit = defineEmits<{
  close: []
  download: [document: DocumentItem]
}>()

const {t} = useI18n()

const canPreview = computed(() => props.document.format.toUpperCase() === 'PDF')

function onBackdropClick(event: MouseEvent) {
  if (event.target === event.currentTarget) emit('close')
}

</script>

<template>
  <div class="modal-backdrop" @click="onBackdropClick">
    <article class="preview-modal">
      <button class="modal-close" type="button" :aria-label="t('preview.close')" @click="emit('close')">×</button>

      <span class="file-icon blue">{{ document.format }}</span>
      <p class="eyebrow">{{ t('preview.eyebrow') }}</p>
      <h2>{{ document.title }}</h2>
      <p>{{ document.subject }} · {{ document.size }} · {{ t('preview.sharedBy') }} {{ document.author }}</p>

      <object
          v-if="canPreview"
          :data="url"
          type="application/pdf"
          class="preview-frame"
      >
        <p class="preview-placeholder">
          {{ t('preview.unavailable') }}
          <a :href="url" target="_blank" rel="noopener">{{ t('preview.openNewTab') }}</a>
        </p>
      </object>

      <p v-else class="preview-placeholder">
        {{ t('preview.unsupported') }}
      </p>

      <AnnalisButton
          :label="t('preview.download')"
          variant="primary"
          :icon="{ icon: 'Download', leading: true }"
          @click="emit('download', document)"
      />
    </article>
  </div>
</template>

<style scoped>

.modal-backdrop {
  position: fixed;
  z-index: 10;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 20px;
  background: #102b2480
}

.preview-modal {
  position: relative;
  width: min(900px, 100%);
  max-height: 92vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: stretch;      /* ← important pour que l'iframe prenne la largeur */
  gap: 12px;
  padding: 30px;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 20px 60px #102b2450;
}

.preview-frame {
  width: 100%;
  height: 65vh;              /* ← valeur explicite, jamais 100% ici */
  border: none;
  border-radius: 10px;
  background: #f3f5f4;
}

.preview-modal h2 {
  font-size: 22px;
  color: var(--ink)
}

.preview-modal > p:not(.eyebrow) {
  color: var(--muted);
  font-size: 12px
}

.modal-close {
  position: absolute;
  top: 12px;
  right: 15px;
  color: var(--muted);
  background: none;
  font-size: 24px
}

.preview-placeholder {
  display: grid;
  place-items: center;
  width: 100%;
  height: 150px;
  border: 1px solid var(--line);
  border-radius: 10px;
  color: var(--muted);
  background: var(--pale);
  font-size: 12px
}

</style>
