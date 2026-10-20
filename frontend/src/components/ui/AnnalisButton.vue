<script setup lang="ts">

import Icon from "@/components/ui/Icon.vue";

defineProps<{
  label: string
  variant?: 'primary' | 'secondary'
  icon?: {
    icon: string
    leading?: boolean
    size?: number
  }
}>()

</script>

<template>
  <button class="annalis-button" :class="variant">
    <Icon v-if="icon && !icon.leading" :icon="icon.icon" :size="icon.size"/>
    {{ label }}
    <Icon v-if="icon && icon.leading" :icon="icon.icon" :size="icon.size"/>
  </button>
</template>

<style scoped>
.annalis-button {
  min-height: 43px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  padding: 0 19px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap
}

.annalis-button.primary {
  color: #fff;
  background: var(--green);
  box-shadow: 0 5px 7px #173f3529
}

.annalis-button.secondary, .annalis-button.pale {
  color: var(--green);
  background: var(--pale)
}

</style>