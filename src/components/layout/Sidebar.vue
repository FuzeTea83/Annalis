<script setup lang="ts">
import { computed } from 'vue'
import type { NavItem, View } from '@/types/views'
import { useI18n } from "vue-i18n"
import { useRoute } from 'vue-router'
import Brand from "@/components/ui/Brand.vue"
import { useAuthStore } from "@/stores/auth"
import Avatar from "@/components/ui/Avatar.vue";
import Icon from "@/components/ui/Icon.vue";

const { t } = useI18n()
const route = useRoute()
const auth = useAuthStore()

defineProps<{
  navItems: NavItem[]
}>()

const emit = defineEmits<{
  navigate: [view: View]
}>()

const userName = computed(() => auth.user?.name ?? '')
const userInitials = computed(() => {
  if (auth.user?.initials) return auth.user.initials
  return ''
})

async function handleLogout() {
  await auth.logout()
}
</script>

<template>
  <aside class="sidebar">
    <Brand />
    <nav class="sidebar-nav" :aria-label="t('sidebar.navigation')">
      <p class="nav-caption">{{ t('sidebar.studentSpace') }}</p>
      <router-link
        v-for="item in navItems"
        :key="item.id"
        :to="{ name: item.id }"
        class="sidebar-button"
        :class="{ active: route.name === item.id }"
      >
        <Icon :icon="item.icon" />
        <span>{{ item.label }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <router-link class="profile-card" to="/account">
        <Avatar :user-initials="userInitials" :large="true"/>
        <span class="profile-copy">
          <strong>{{ userName }}</strong>
        </span>
        <Icon class="more-icon" icon="Arrow" />
      </router-link>
      <button class="logout-button" type="button" @click="handleLogout">
        <Icon icon="Door" :size="17"/>
        {{ t('sidebar.disconnect') }}
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 256px;
  flex: 0 0 256px;
  display: flex;
  flex-direction: column;
  padding: 30px 22px 24px;
  color: #fff;
  background: var(--green);
  position: static;
}

.sidebar-nav {
  padding-top: 54px
}

.nav-caption, .eyebrow {
  margin: 0;
  color: #9db4ab;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 2px
}

.sidebar-button {
  width: 212px;
  min-height: 47px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 13px;
  border-radius: 11px;
  color: #c6d4cf;
  background: transparent;
  text-align: left;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
}

.sidebar-button + .sidebar-button {
  margin-top: 7px
}

.sidebar-button.active {
  color: #fff;
  background: rgba(255, 255, 255, .1);
  box-shadow: inset 2px 0 var(--coral)
}

.sidebar-footer {
  margin-top: auto
}

.profile-card {
  width: 212px;
  min-height: 58px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border: 1px solid rgba(255, 255, 255, .11);
  border-radius: 12px;
  color: #fff;
  background: rgba(255, 255, 255, .05);
  text-align: left;
  text-decoration: none;
}

.profile-copy {
  display: flex;
  flex-direction: column;
  min-width: 0
}

.profile-copy strong {
  font-size: 12px
}

.profile-copy small {
  margin-top: 3px;
  color: #aabdb6;
  font-size: 10px
}

.more-icon {
  margin-left: auto;
  color: #aabdb6;
  font-size: 20px
}

.logout-button {
  display: flex;
  align-items: center;
  gap: 9px;
  width: 100%;
  padding: 12px 10px 6px;
  color: #9db4ab;
  background: none;
  font-size: 12px;
  text-align: left
}

@media (max-width: 1000px) {
  .sidebar {
    width: 220px;
    flex-basis: 220px
  }

  .sidebar-button, .profile-card {
    width: 176px
  }
}

@media (max-width: 720px) {
  .sidebar {
    display: none
  }
}

</style>