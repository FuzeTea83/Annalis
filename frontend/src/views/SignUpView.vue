<script setup lang="ts">
import { reactive } from 'vue'
import { useRoute, } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ApiError } from "@/api/http"
import { useI18n } from "vue-i18n"
import AuthPromo from "@/components/layout/AuthPromo.vue";

const auth = useAuthStore()
const route = useRoute()
const { t, locale } = useI18n()

const form = reactive({ firstName: '', lastName: '', email: '', password: '' })
const fieldErrors = reactive<Record<string, string[]>>({})

Object.keys(fieldErrors).forEach((k) => delete fieldErrors[k])

async function submit() {
  Object.keys(fieldErrors).forEach((k) => delete fieldErrors[k])
  try {
    const redirectTo = (route.query.redirect as string) ?? '/'
    await auth.register(form, redirectTo)
  } catch (e) {
    if (e instanceof ApiError && e.errors) {
      Object.assign(fieldErrors, e.errors)
    }
  }
}
</script>

<template>
  <div class="auth-page">
    <label class="language-select">
      <span class="sr-only">{{ t('label.language') }}</span>
      <select v-model="locale" :aria-label="t('label.language')">
        <option value="fr-FR">FR</option>
        <option value="en-US">EN</option>
      </select>
    </label>
    <AuthPromo/>

    <div class="auth-form-side">
      <div class="auth-card">
        <p class="auth-eyebrow">{{ t('auth.welcome') }}</p>
        <h2 class="auth-title">{{ t('auth.signupTitle') }}</h2>
        <p class="auth-subtitle">{{ t('auth.signupSubtitle') }}</p>

        <p v-if="auth.error" class="alert-error">{{ auth.error }}</p>

        <form @submit.prevent="submit" class="auth-form">
          <div class="auth-form-name-grid">
            <label class="auth-field">
              <span>{{ t('auth.firstName') }}</span>
              <input
                  v-model="form.firstName"
                  type="text"
                  autocomplete="name"
                  :placeholder="t('auth.firstNamePlaceholder')"
                  required
              />
              <small v-for="msg in fieldErrors.firstName" :key="msg" class="field-error">{{ msg }}</small>
            </label>

            <label class="auth-field">
              <span>{{ t('auth.lastName') }}</span>
              <input
                  v-model="form.lastName"
                  type="text"
                  autocomplete="name"
                  :placeholder="t('auth.lastNamePlaceholder')"
                  required
              />
              <small v-for="msg in fieldErrors.lastName" :key="msg" class="field-error">{{ msg }}</small>
            </label>
          </div>


          <label class="auth-field">
            <span>{{ t('auth.email') }}</span>
            <input
              v-model="form.email"
              type="email"
              autocomplete="email"
              :placeholder="t('auth.emailPlaceholder')"
              required
            />
            <small v-for="msg in fieldErrors.email" :key="msg" class="field-error">{{ msg }}</small>
          </label>

          <label class="auth-field">
            <span>{{ t('auth.password') }}</span>
            <input
              v-model="form.password"
              type="password"
              autocomplete="new-password"
              :placeholder="t('auth.passwordPlaceholder')"
              required
            />
            <small v-for="msg in fieldErrors.password" :key="msg" class="field-error">{{ msg }}</small>
          </label>

          <button type="submit" class="auth-submit-btn" :disabled="auth.loading">
            <span>{{ auth.loading ? t('auth.signingUp') : t('auth.signup') }}</span>
            <span class="arrow-icon">→</span>
          </button>
        </form>

        <div class="auth-switch">
          <span>{{ t('auth.existingAccount') }} </span>
          <router-link to="/login" class="auth-link">{{ t('auth.login') }}</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  position: relative;
  display: grid;
  grid-template-columns: 48% 52%;
  min-height: 100vh;
  background: #fff;
}

.language-select {
  position: absolute;
  top: 24px;
  right: 32px;
  z-index: 1;
}

.language-select select {
  padding: 6px 8px;
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

.auth-form-side {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 32px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
}

.auth-eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--coral);
  margin-bottom: 12px;
  text-transform: uppercase;
}

.auth-title {
  font-size: 34px;
  font-weight: 700;
  color: var(--ink);
  letter-spacing: -0.8px;
  margin-bottom: 8px;
}

.auth-subtitle {
  font-size: 14px;
  color: var(--muted);
  margin-bottom: 32px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.auth-form-name-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.auth-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink);
}

.auth-field input {
  width: 100%;
  padding: 13px 16px;
  border: 1px solid var(--line);
  border-radius: 12px;
  font-size: 14px;
  outline: none;
  background: #fff;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.auth-field input:focus {
  border-color: var(--green);
  box-shadow: 0 0 0 3px rgba(22, 51, 40, 0.1);
}

.auth-submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
  padding: 14px 24px;
  border-radius: 12px;
  border: none;
  background: var(--green);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s ease, transform 0.1s ease;
}

.auth-submit-btn:hover:not(:disabled) {
  opacity: 0.94;
  transform: translateY(-1px);
}

.auth-submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.arrow-icon {
  font-size: 16px;
  transition: transform 0.2s ease;
}

.auth-submit-btn:hover:not(:disabled) .arrow-icon {
  transform: translateX(3px);
}

.auth-switch {
  margin-top: 28px;
  text-align: center;
  font-size: 13px;
  color: var(--muted);
}

.auth-link {
  font-weight: 700;
  color: var(--ink);
  text-decoration: underline;
  margin-left: 4px;
}

.alert-error {
  padding: 12px 14px;
  border-radius: 8px;
  background: #fee2e2;
  color: #991b1b;
  font-size: 13px;
  margin-bottom: 20px;
}

.field-error {
  color: #dc2626;
  font-size: 12px;
  margin-top: 4px;
}

@media (max-width: 900px) {
  .auth-page {
    grid-template-columns: 1fr;
  }

  .auth-form-side {
    padding: 60px 24px;
  }
}
</style>
