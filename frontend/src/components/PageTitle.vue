<script setup lang="ts">
defineProps<{
  eyebrow: string
  title: string
  subtitle: string
}>()
</script>

<template>
  <section class="page-title">
    <p class="eyebrow">{{ eyebrow }}</p>
    <h1>{{ title }}</h1>
    <p class="subtitle">{{ subtitle }}</p>
  </section>
</template>

<style scoped>
.page-title {
  margin-bottom: 38px
}

.page-title h1 {
  margin: 7px 0 4px;
  font-weight: 400;
  font-size: 40px;
  line-height: 1.15;
  letter-spacing: -1.1px;
  color: var(--ink)
}

.subtitle {
  margin: 0;
  color: var(--muted);
  font-size: 15px
}

@media (max-width: 720px) {
  .page-title h1 {
    font-size: 34px
  }
}


</style>