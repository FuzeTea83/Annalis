<script setup lang="ts">
import {useI18n} from "vue-i18n";

const { t } = useI18n()

</script>

<template>
  <div class="auth-promo">
    <div class="promo-brand">
        <span class="promo-logo" aria-hidden="true">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
            <path d="M6 12v5c3 3 9 3 12 0v-5"/>
          </svg>
        </span>
      <span class="promo-brand-text">Annalis</span>
    </div>

    <div class="promo-center">
      <p class="promo-eyebrow">{{ t('auth.promoEyebrow') }}</p>
      <h1 class="promo-title">{{ t('auth.promoTitle') }}</h1>
      <p class="promo-text">{{ t('auth.promoText') }}</p>
    </div>
  </div>

</template>

<style scoped>

.auth-promo {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 60px 80px;
  background: var(--green);
  color: #fff;
  overflow: hidden;
}

.auth-promo::before {
  content: '';
  position: absolute;
  top: 15%;
  right: -100px;
  width: 480px;
  height: 480px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.05) 0%, transparent 70%);
  pointer-events: none;
}

.promo-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.promo-logo {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: var(--coral);
  color: #fff;
}

.promo-brand-text {
  font-weight: 800;
  font-size: 22px;
  letter-spacing: -0.5px;
}

.promo-center {
  max-width: 480px;
  margin: 40px 0 300px 0;
}

.promo-eyebrow {
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 2px;
  color: var(--coral);
  margin-bottom: 20px;
  text-transform: uppercase;
}

.promo-title {
  font-size: 54px;
  font-weight: 400;
  line-height: 1.15;
  color: #fff;
  margin-bottom: 24px;
  letter-spacing: -1px;
}

.promo-text {
  font-size: 16px;
  line-height: 1.6;
  color: var(--mint);
  max-width: 420px;
}

@media (max-width: 900px) {
  .auth-promo {
    display: none;
  }
}
</style>