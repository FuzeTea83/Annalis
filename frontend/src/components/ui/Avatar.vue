<script setup lang="ts">

defineProps<{
  userInitials: string,
  large?: boolean,
  green?: boolean,
}>()

</script>

<template>
  <span class="avatar avatar-cream" :class="{ 'avatar-large': large, 'avatar-green': green }">{{ userInitials }}</span>
</template>

<style scoped>
.avatar {
  display: inline-grid;
  place-items: center;
  width: 36px;
  height: 36px;
  flex: 0 0 36px;
  border-radius: 50%;
  font-size: 11px;
  font-weight: 800
}

.avatar-cream {
  color: var(--green);
  background: var(--cream)
}

.avatar-green {
  width: 27px;
  height: 27px;
  flex-basis: 27px;
  color: var(--green);
  background: var(--mint);
  font-size: 9px
}

.avatar-large {
  width: 50px;
  height: 50px;
  flex-basis: 50px;
  font-size: 14px
}


</style>