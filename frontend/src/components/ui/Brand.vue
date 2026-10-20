<script setup lang="ts">
import Icon from "@/components/ui/Icon.vue";
</script>
<template>
  <router-link to="/" class="brand">
    <span class="brand-mark" aria-hidden="true">
      <Icon icon="Brand" :size="22" />
    </span>
    <span class="brand-name">Annalis</span>
  </router-link>
</template>

<style scoped>
.brand {
  display: flex;
  align-items: center;
  gap: 11px;
  color: white;
  background: none;
  text-align: left;
  text-decoration: none;
}

.brand-mark {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  color: #fff;
  background: var(--coral);
  font-size: 20px
}

.brand-name {
  font-weight: 800;
  font-size: 22px;
  letter-spacing: -.8px;
}

</style>