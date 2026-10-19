<script setup lang="ts">
import type {DocumentItem} from '@/types/document'
import {useI18n} from "vue-i18n"
import Avatar from "@/components/ui/Avatar.vue";
import Icon from "@/components/ui/Icon.vue";
import {computed} from "vue";

const {t} = useI18n()

const props = defineProps<{ document: DocumentItem }>()

const emit = defineEmits<{
  preview: [document: DocumentItem]
  download: [document: DocumentItem]
  report: [document: DocumentItem]
}>()

const initials = computed(() => {
  const f = props.document.author.split(' ')[0]?.[0]?.toUpperCase() || ''
  const l = props.document.author.split(' ')[1]?.[0]?.toUpperCase() || ''
  return `${f}${l}` || 'NA'
})

const tone = computed(() => {
  switch (props.document.format.toUpperCase()) {
    case 'PDF':
      return 'blue'
    case 'DOCX':
      return 'purple'
    case 'PPTX':
      return 'coral'
    default:
      return 'green'
  }
})

const size = computed(() => {
  if (props.document.size < 1024) return props.document.size
  if (props.document.size < 1024 * 1024) return (props.document.size / 1024).toFixed(0) + ' KB'
  return (props.document.size / (1024 * 1024)).toFixed(0) + ' MB'
})

const formatedDate = computed(() => {
  const date = new Date(props.document.createdAt)
  return date.toLocaleDateString('fr-FR', {day: 'numeric', month: 'short', year: 'numeric'})
})

</script>

<template>
  <div class="document-row">
    <span class="file-icon" :class="tone">{{ document.format.toUpperCase() }}</span>
    <div class="document-copy">
      <strong>{{ document.title }}</strong>
      <span>{{ document.subject }} · {{ document.format.toUpperCase() }} · {{ size }}</span>
    </div>
    <div class="author">
      <Avatar :user-initials="initials" :green="true"/>
      <span>{{ document.author }}</span>
    </div>
    <span class="document-date">{{ formatedDate }}</span>
    <div class="row-actions">
      <button
          type="button"
          :title="t('label.visualise')"
          :aria-label="t('label.visualise')"
          @click="emit('preview', document)"
      >
        <Icon icon="Eye" :size="17"/>
      </button>
      <button
          type="button"
          :title="t('label.download')"
          :aria-label="t('label.download')"
          @click="emit('download', document)"
      >
        <Icon icon="Download" :size="17"/>
      </button>
      <button
          type="button"
          :title="t('label.report')"
          :aria-label="t('label.report')"
          @click="emit('report', document)"
      >
        <Icon icon="Report" :size="17"/>
      </button>
    </div>
  </div>
</template>

<style scoped>

.document-copy {
  display: flex;
  flex-direction: column;
  min-width: 0
}

.document-copy strong {
  overflow: hidden;
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--ink);
  font-weight: 700;
}

.document-copy span, .document-date {
  color: var(--muted);
  font-size: 11px
}

.document-copy span {
  margin-top: 5px
}

.document-row {
  position: relative;
  display: grid;
  align-items: center;
  column-gap: 14px;
  padding: 14px 18px;
  border-bottom: 1px solid var(--line);
  grid-template-columns:42px minmax(220px, 1.7fr) minmax(130px, .8fr) 105px auto;
  min-height: 70px;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
}

.document-row:last-child {
  border-bottom: 0
}

.author {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--ink);
  font-size: 11px
}

.row-actions {
  display: flex;
  gap: 4px;
  justify-content: end
}

.row-actions button {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  color: var(--green);
  background: var(--pale);
  font-weight: 700
}


@media (max-width: 1000px) {
  .document-row {
    grid-template-columns:42px minmax(180px, 1fr) auto
  }

  .author, .document-date, .explorer-row .author, .explorer-row .document-date {
    display: none
  }

  .document-row .row-actions {
    grid-column: 3;
    grid-row: 1
  }
}


@media (max-width: 720px) {
  .document-row {
    grid-template-columns:42px minmax(0, 1fr)
  }

  .row-actions, .document-row .row-actions {
    grid-column: 2;
    justify-content: start
  }
}

</style>

