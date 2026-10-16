<script setup lang="ts">
import { reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ApiError } from "@/api/http"

const auth = useAuthStore()
const route = useRoute()

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
        <p class="promo-eyebrow">LA BIBLIOTHÈQUE DE TA PROMO</p>
        <h1 class="promo-title">Apprendre mieux,<br />ensemble.</h1>
        <p class="promo-text">
          Retrouve les meilleures ressources de cours, partagées et vérifiées par ta communauté étudiante.
        </p>
      </div>

      <div class="promo-footer">
        <div class="avatar-group">
          <span class="avatar-bubble avatar-lm">LM</span>
          <span class="avatar-bubble avatar-ar">AR</span>
          <span class="avatar-bubble avatar-more">+2k</span>
        </div>
        <div class="social-proof-copy">
          <strong>2 400+ étudiants</strong>
          <span>partagent déjà leurs notes</span>
        </div>
      </div>
    </div>

    <div class="auth-form-side">
      <div class="auth-card">
        <p class="auth-eyebrow">BIENVENUE SUR ANNALIS</p>
        <h2 class="auth-title">Rejoins ta communauté.</h2>
        <p class="auth-subtitle">Crée ton compte étudiant en quelques secondes.</p>

        <p v-if="auth.error" class="alert-error">{{ auth.error }}</p>

        <form @submit.prevent="submit" class="auth-form">
          <div class="auth-form-name-grid">
            <label class="auth-field">
              <span>Prénom</span>
              <input
                  v-model="form.firstName"
                  type="text"
                  autocomplete="name"
                  placeholder="Camille"
                  required
              />
              <small v-for="msg in fieldErrors.firstName" :key="msg" class="field-error">{{ msg }}</small>
            </label>

            <label class="auth-field">
              <span>Nom</span>
              <input
                  v-model="form.lastName"
                  type="text"
                  autocomplete="name"
                  placeholder="Dupont"
                  required
              />
              <small v-for="msg in fieldErrors.lastName" :key="msg" class="field-error">{{ msg }}</small>
            </label>
          </div>


          <label class="auth-field">
            <span>Adresse e-mail</span>
            <input
              v-model="form.email"
              type="email"
              autocomplete="email"
              placeholder="prenom.nom@universite.fr"
              required
            />
            <small v-for="msg in fieldErrors.email" :key="msg" class="field-error">{{ msg }}</small>
          </label>

          <label class="auth-field">
            <span>Mot de passe</span>
            <input
              v-model="form.password"
              type="password"
              autocomplete="new-password"
              placeholder="8 caractères minimum"
              required
            />
            <small v-for="msg in fieldErrors.password" :key="msg" class="field-error">{{ msg }}</small>
          </label>

          <button type="submit" class="auth-submit-btn" :disabled="auth.loading">
            <span>{{ auth.loading ? 'Création du compte…' : 'Créer mon compte' }}</span>
            <span class="arrow-icon">→</span>
          </button>
        </form>

        <div class="auth-switch">
          <span>Déjà inscrit·e ? </span>
          <router-link to="/login" class="auth-link">Se connecter</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  display: grid;
  grid-template-columns: 48% 52%;
  min-height: 100vh;
  background: #fff;
}

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
  margin: 40px 0;
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

.promo-footer {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar-group {
  display: flex;
  align-items: center;
}

.avatar-bubble {
  display: grid;
  place-items: center;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 2px solid var(--green);
  font-size: 12px;
  font-weight: 700;
  margin-left: -8px;
}

.avatar-bubble:first-child {
  margin-left: 0;
}

.avatar-lm {
  background: var(--coral);
  color: #fff;
}

.avatar-ar {
  background: var(--cream);
  color: var(--ink);
}

.avatar-more {
  background: #fff;
  color: var(--green);
}

.social-proof-copy {
  display: flex;
  flex-direction: column;
  font-size: 13px;
  line-height: 1.35;
}

.social-proof-copy strong {
  color: #fff;
  font-weight: 700;
}

.social-proof-copy span {
  color: var(--mint);
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
  .auth-promo {
    display: none;
  }
  .auth-form-side {
    padding: 60px 24px;
  }
}
</style>
