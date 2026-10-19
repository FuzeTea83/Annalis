import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import router from '@/router'
import { authApi, type Credentials } from '@/api/auth'
import { ApiError } from '@/api/http'
import type { User } from '@/types/user'


export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    const isAuthenticated = computed(() => !!user.value)

    async function login(credentials: Credentials, redirectTo = '/') {
        loading.value = true
        error.value = null
        try {
            const response = await authApi.login(credentials)
            localStorage.setItem('token', response.token)
            user.value = response.user
            await router.push(redirectTo)
        } catch (e) {
            error.value = e instanceof ApiError ? e.message : 'Connexion impossible'
            throw e
        } finally {
            loading.value = false
        }
    }

    async function register(payload: Credentials & { firstName: string; lastName: string }, redirectTo = '/') {
        loading.value = true
        error.value = null
        try {
            const response = await authApi.register(payload)
            localStorage.setItem('token', response.token)
            user.value = response.user
            await router.push(redirectTo)
        } catch (e) {
            error.value = e instanceof ApiError ? e.message : 'Inscription impossible'
            throw e
        } finally {
            loading.value = false
        }
    }

    /** Recharge la session au démarrage (F5, nouvelle visite) */
    async function restoreSession() {
        if (!localStorage.getItem('token')) return
        try {
            user.value = await authApi.me()
        } catch {
            localStorage.removeItem('token')
            user.value = null
        }
    }

    async function logout() {
        try { await authApi.logout() } catch { /* on déconnecte quand même */ }
        localStorage.removeItem('token')
        user.value = null
        await router.push({ name: 'login' })
    }

    return { user, loading, error, isAuthenticated, login, register, logout, restoreSession }
})