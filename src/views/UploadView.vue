<script setup lang="ts">
import {computed, ref} from 'vue'
import PageTitle from '@/components/PageTitle.vue'
import {useDocumentsStore} from '@/stores/documents'
import {documentsApi} from '@/api/documents'
import AnnalisButton from "@/components/ui/AnnalisButton.vue";

const docsStore = useDocumentsStore()

const selectedFile = ref<File | null>(null)
const title = ref('')
const description = ref('')
const subject = ref('')
const sector = ref('Licence 1')
const sector_year = ref('Licence 1')
const school_year = ref('Licence 1')
const session = ref<1 | 2 | null>(null)
const message = ref('')
const isSuccess = ref(false)

const schoolYears = computed(() => {
  const currentYear = new Date().getFullYear()
  return Array.from({ length: 5 }, (_, i) => `${currentYear + i}/${currentYear + i + 1}`)
})

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0]
    message.value = ''
    if (!title.value) {
      title.value = target.files[0].name.replace(/\.[^/.]+$/, '').replaceAll('-', ' ')
    }
  }
}

function handleDrop(event: DragEvent) {
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    selectedFile.value = event.dataTransfer.files[0]
    message.value = ''
    if (!title.value) {
      title.value = event.dataTransfer.files[0].name.replace(/\.[^/.]+$/, '').replaceAll('-', ' ')
    }
  }
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024 * 1024) {
    return `${Math.round(bytes / 1024)} Ko`
  }
  return `${(bytes / (1024 * 1024)).toFixed(1).replace('.', ',')} Mo`
}

async function submitForm() {
  if (!selectedFile.value) {
    isSuccess.value = false
    message.value = 'Sélectionne un fichier (PDF, DOCX ou PPTX) pour continuer.'
    return
  }
  if (!title.value.trim() || !subject.value) {
    isSuccess.value = false
    message.value = 'Renseigne un titre et choisis une matière.'
    return
  }

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  formData.append('title', title.value.trim())
  formData.append('description', description.value)
  formData.append('subject', subject.value)
  formData.append('sector', sector.value)
  formData.append('sector_year', String(sector_year.value.match(/(\d+)/)?.[0] || '1'))
  formData.append('school_year', String(school_year.value.match(/(\d+)/)?.[0] || '2000'))
  formData.append('session', String(session.value ?? ''))

  try {
    const newDocument = await documentsApi.upload(formData)
    docsStore.addDocument(newDocument)
    isSuccess.value = true
    message.value = 'Ton document a été transmis avec succès et ajouté à la bibliothèque.'
    selectedFile.value = null
    title.value = ''
    subject.value = ''
    sector.value = ''
    sector_year.value = ''
    school_year.value = ''
    session.value = null
    description.value = ''
  } catch (error) {
    isSuccess.value = false
    message.value = error instanceof Error ? error.message : 'L’envoi du document a échoué.'
  }
}
</script>

<template>
  <PageTitle
    eyebrow="CONTRIBUER"
    title="Déposer un document"
    subtitle="Partage une ressource utile avec ta communauté étudiante."
  />

  <form class="upload-card" @submit.prevent="submitForm">
    <div class="form-step">
      <span class="step-number">1</span>
      <div class="step-content">
        <h2>Ton fichier</h2>
        <p>Formats acceptés : PDF, DOCX ou PPTX · 20 Mo maximum</p>

        <label
          class="drop-zone"
          @dragover.prevent
          @drop.prevent="handleDrop"
        >
          <input
            type="file"
            accept=".pdf,.docx,.pptx"
            @change="onFileChange"
          />
          <span class="upload-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
          </span>
          <strong>{{ selectedFile ? selectedFile.name : 'Glisse ton fichier ici' }}</strong>
          <small>{{ selectedFile ? formatFileSize(selectedFile.size) : 'ou clique pour le parcourir' }}</small>
        </label>
      </div>
    </div>

    <div class="form-divider"></div>

    <div class="form-step">
      <span class="step-number">2</span>
      <div class="step-content">
        <h2>Informations du document</h2>
        <div class="form-grid">
          <label class="form-label full">
            Titre du document
            <input
              v-model="title"
              placeholder="Ex. Fiche de révision — Algorithmes de tri"
              required
            />
          </label>

          <label class="form-label">
            Matière
            <select v-model="subject" required>
              <option value="" disabled>Choisir une matière</option>
              <option>Algorithmique</option>
              <option>Mathématiques</option>
              <option>Informatique</option>
              <option>Économie</option>
              <option>Droit</option>
            </select>
          </label>

          <label class="form-label">
            Section
            <select v-model="sector">
              <option value="" disabled>Choisir une section</option>
              <option>Informatique</option>
              <option>Matériaux</option>
              <option>Peip</option>
            </select>
          </label>

          <label class="form-label">
            Niveau
            <select v-model="sector_year">
              <option>Licence 1</option>
              <option>Licence 2</option>
              <option>Licence 3</option>
              <option>Master 1</option>
              <option>Master 2</option>
            </select>
          </label>

          <label class="form-label">
            Année scolaire
            <select v-model="school_year">
              <option value="" disabled>Choisir une année scolaire</option>
              <option v-for="year in schoolYears" :key="year">{{ year }}</option>
            </select>
          </label>

          <label class="form-label full">
            Description <span>(facultatif)</span>
            <textarea
              v-model="description"
              placeholder="Ajoute quelques mots pour aider les étudiants à comprendre le contenu..."
              rows="3"
            ></textarea>
          </label>
        </div>
      </div>
    </div>

    <!-- Footer de validation -->
    <div class="upload-footer">
      <span class="verification-note">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          <path d="m9 12 2 2 4-4"/>
        </svg>
        Ton document sera vérifié avant sa publication.
      </span>

      <AnnalisButton label="Envoyer pour validation" variant="primary" :icon="{icon: 'Arrow', leading: true}"/>
    </div>

    <p v-if="message" class="form-message" :class="{ 'message-success': isSuccess, 'message-error': !isSuccess }">
      {{ message }}
    </p>
  </form>
</template>

<style scoped>
.verification-note {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--muted);
  font-size: 13px;
}

.verification-note svg {
  color: var(--green);
}

.upload-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--pale);
  color: var(--green);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.message-success {
  color: #166534;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 16px 36px;
}

.message-error {
  color: #991b1b;
  background: #fee2e2;
  border: 1px solid #fecaca;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 16px 36px;
}

.upload-card {
  border: 1px solid var(--line);
  border-radius: 14px;
  background: #fff;
  box-shadow: 0 8px 20px #173f3508
}

.upload-card {
  overflow: hidden
}

.form-step {
  display: flex;
  gap: 18px;
  padding: 28px 30px
}

.step-number {
  display: grid;
  place-items: center;
  width: 23px;
  height: 23px;
  flex: 0 0 23px;
  border-radius: 50%;
  color: #fff;
  background: var(--green);
  font-size: 11px
}

.step-content {
  flex: 1
}

.step-content h2, .account-card h2 {
  font-size: 15px;
  font-weight: 500;
  color: var(--ink)
}

.step-content p {
  margin: 3px 0 15px;
  color: var(--muted);
  font-size: 11px
}

.drop-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 120px;
  border: 1px dashed #b8c9c0;
  border-radius: 11px;
  background: #fcfdfb;
  color: var(--ink);
  cursor: pointer
}

.drop-zone input {
  display: none
}

.upload-icon {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  color: var(--green);
  background: var(--mint);
  font-size: 20px
}

.drop-zone small {
  color: var(--muted);
  font-size: 10px
}

.form-divider {
  height: 1px;
  margin: 0 30px;
  background: var(--line)
}
</style>
