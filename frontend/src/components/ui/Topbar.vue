<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth.ts'
import Avatar from "@/components/ui/Avatar.vue";
import { useI18n } from 'vue-i18n'

const auth = useAuthStore()
const { locale, t } = useI18n()

defineProps<{
  title: string
}>()

const initials = computed(() => {
  if (auth.user?.initials) return auth.user.initials
  if (auth.user?.firstName) {
    return auth.user.firstName[0]?.toUpperCase() || '' + auth.user.lastName[0]?.toUpperCase() || ''
  }
  return ''
})
</script>

<template>
  <header class="topbar">
    <strong>{{ title }}</strong>
    <div class="topbar-actions">
      <label class="language-select">
        <span class="sr-only">{{ t('label.language') }}</span>
        <select v-model="locale" :aria-label="t('label.language')">
          <option value="fr-FR">FR</option>
          <option value="en-US">EN</option>
        </select>
      </label>
      <router-link to="/account" class="avatar-button" :aria-label="t('label.account')">
        <Avatar :user-initials="initials" />
      </router-link>
    </div>
  </header>
</template>

<style scoped>
.topbar {
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 64px;
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, .82);
  backdrop-filter: blur(12px)
}

.topbar > strong {
  font-weight: 700;
  font-size: 13px;
  color: var(--ink);
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 12px
}

.avatar-button {
  border: 0
}

.language-select select {
  padding: 5px 7px;
  border: 1px solid var(--line);
  border-radius: 6px;
  color: var(--muted);
  background: #fff;
  font-size: 11px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@media (max-width: 1000px) {
  .topbar {
    padding: 0 32px
  }
}

@media (max-width: 720px) {
  .topbar {
    padding: 0 20px
  }
}
</style>