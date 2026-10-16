import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import {useAuthStore} from "@/stores/auth.ts";

const routes = [
    {
        path: '/',
        name: 'overview',
        alias: '/overview',
        component: HomeView,
        meta: { title: "Vue d'ensemble", requiresAuth: true },
    },
    {
        path: '/account',
        name: 'account',
        component: () => import('@/views/AccountView.vue'),
        meta: { title: 'Mon compte', requiresAuth: true }
    },
    {
        path: '/explorer',
        name: 'explorer',
        component: () => import('@/views/ExplorerView.vue'),
        meta: { title: 'Explorer', requiresAuth: true }
    },
    {
        path: '/upload',
        name: 'upload',
        component: () => import('@/views/UploadView.vue'),
        meta: { title: 'Déposer un document', requiresAuth: true }
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('@/views/LoginView.vue'),
        meta: { title: 'Connexion', requiresAuth: false, hideNavigation: true }
    },
    {
        path: '/sign-up',
        name: 'sign-up',
        component: () => import('@/views/SignUpView.vue'),
        meta: { title: 'Inscription', requiresAuth: false, hideNavigation: true }
    },
    {
        path: '/:pathMatch(.*)*',  // route 404
        name: 'not-found',
        component: () => import('@/views/NotFoundView.vue'),
        meta: { title: 'Page introuvable', requiresAuth: false }
    }
]



const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

router.beforeEach(async (to) => {
    const auth = useAuthStore()

    // Restaure la session une seule fois (après un F5)
    if (!auth.user && localStorage.getItem('token')) await auth.restoreSession()

    const needsAuth = to.meta.requiresAuth || to.meta.requireAuth
    if (needsAuth && !auth.isAuthenticated) {
        return { name: 'login', query: { redirect: to.fullPath } }
    }
    if ((to.name === 'login' || to.name === 'sign-up') && auth.isAuthenticated) {
        return { name: 'overview' }
    }
})

export default router