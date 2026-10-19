<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import PageTitle from '../components/PageTitle.vue'
import { useAuthStore } from '@/stores/auth'
import Avatar from "@/components/ui/Avatar.vue";

const auth = useAuthStore()

const activeTab = ref<'info' | 'notifications' | 'privacy'>('info')
const message = ref('')

const form = reactive({
  firstName: auth.user?.firstName || 'Camille',
  lastName: auth.user?.lastName || 'Moreau',
  email: auth.user?.email || 'camille.moreau@univ-lyon.fr',
})

const fullName = computed(() => `${form.firstName} ${form.lastName}`.trim())
const initials = computed(() => {
  const f = form.firstName[0]?.toUpperCase() || ''
  const l = form.lastName[0]?.toUpperCase() || ''
  return `${f}${l}` || 'CM'
})

function saveProfile() {
  if (auth.user) {
    auth.user.firstName = form.firstName
    auth.user.lastName = form.lastName
    auth.user.firstName = fullName.value
    auth.user.email = form.email
    auth.user.initials = initials.value
  }
  message.value = 'Tes informations ont bien été enregistrées.'
  setTimeout(() => {
    message.value = ''
  }, 4000)
}
</script>

<template>
  <PageTitle
    eyebrow="MON ESPACE"
    title="Compte & paramètres"
    subtitle="Gère tes informations et tes préférences."
  />

  <div class="account-card account-summary">
    <Avatar :user-initials="initials" :large="true"/>
    <div class="summary-details">
      <h2>{{ fullName }}</h2>
      <p>{{ form.email }}</p>
    </div>
    <button class="notely-button secondary change-photo-btn" type="button">
      Changer la photo
    </button>
  </div>

  <div class="account-layout">
    <aside class="account-tabs">
      <button
        type="button"
        :class="{ selected: activeTab === 'info' }"
        @click="activeTab = 'info'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
          <circle cx="12" cy="7" r="4"/>
        </svg>
        <span>Informations</span>
      </button>

      <button
        type="button"
        :class="{ selected: activeTab === 'notifications' }"
        @click="activeTab = 'notifications'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
        </svg>
        <span>Notifications</span>
      </button>

      <button
        type="button"
        :class="{ selected: activeTab === 'privacy' }"
        @click="activeTab = 'privacy'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
        <span>Confidentialité</span>
      </button>
    </aside>

    <form class="account-card account-form" @submit.prevent="saveProfile">
      <template v-if="activeTab === 'info'">
        <h2>Informations personnelles</h2>
        <p>Mets à jour les informations visibles sur ton profil.</p>

        <div class="form-grid">
          <label class="form-label">
            Prénom
            <input v-model="form.firstName" required />
          </label>

          <label class="form-label">
            Nom
            <input v-model="form.lastName" required />
          </label>

          <label class="form-label full">
            Adresse e-mail
            <input v-model="form.email" type="email" required />
          </label>

        </div>

        <div class="form-submit">
          <button class="notely-button primary" type="submit">
            Enregistrer
          </button>
          <span v-if="message" class="form-message save-success">
            {{ message }}
          </span>
        </div>
      </template>

      <template v-else-if="activeTab === 'notifications'">
        <h2>Préférences de notification</h2>
        <p>Gère la manière dont Annalis t'informe des nouveaux cours et téléchargements.</p>
        <div class="notification-options">
          <label class="pref-checkbox">
            <input type="checkbox" checked />
            <span>Nouveaux documents disponibles dans ma filière</span>
          </label>
          <label class="pref-checkbox">
            <input type="checkbox" checked />
            <span>Validation de mes contributions</span>
          </label>
          <label class="pref-checkbox">
            <input type="checkbox" />
            <span>Rappels de révision hebdomadaires</span>
          </label>
        </div>
        <div class="form-submit">
          <button class="notely-button primary" type="button" @click="saveProfile">
            Enregistrer
          </button>
          <span v-if="message" class="form-message save-success">{{ message }}</span>
        </div>
      </template>

      <template v-else>
        <h2>Confidentialité et données</h2>
        <p>Contrôle les informations partagées avec la communauté étudiante.</p>
        <div class="notification-options">
          <label class="pref-checkbox">
            <input type="checkbox" checked />
            <span>Afficher mon nom complet sur mes documents partagés</span>
          </label>
          <label class="pref-checkbox">
            <input type="checkbox" checked />
            <span>Autoriser les autres étudiants à voir mon niveau d'études</span>
          </label>
        </div>
        <div class="form-submit">
          <button class="notely-button primary" type="button" @click="saveProfile">
            Enregistrer
          </button>
          <span v-if="message" class="form-message save-success">{{ message }}</span>
        </div>
      </template>
    </form>
  </div>
</template>

<style scoped>
.account-tabs button {
  display: flex;
  align-items: center;
  gap: 10px;
}

.summary-details {
  display: flex;
  flex-direction: column;
}

.summary-details h2 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 4px;
}

.summary-details p {
  font-size: 14px;
  color: var(--muted);
  margin-bottom: 8px;
}

.change-photo-btn {
  margin-left: auto;
}

.notification-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 24px 0 32px;
}

.pref-checkbox {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: var(--ink);
  cursor: pointer;
}

.save-success {
  color: #166534;
  font-size: 13px;
  font-weight: 600;
}
</style>

