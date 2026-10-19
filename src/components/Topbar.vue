<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Avatar from "@/components/ui/Avatar.vue";

const auth = useAuthStore()

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
      <router-link to="/account" class="avatar-button" aria-label="Mon compte">
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