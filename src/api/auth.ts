import { api } from '@/api/http'
import type { User } from '@/types/user'

export interface Credentials { email: string; password: string }

export interface AuthResponse {
    token: string
    user: User
}

export const authApi = {
    login: (credentials: Credentials) =>
        api.post<AuthResponse>('/auth/login', credentials, { auth: false }),

    register: (payload: Credentials & { firstName: string; lastName: string }, redirectTo = '/') =>
        api.post<AuthResponse>('/auth/register', payload, { auth: false }),

    me: () => api.get<User>('/auth/me'),

    logout: () => api.post<void>('/auth/logout'),

    forgotPassword: (email: string) =>
        api.post<void>('/auth/forgot-password', { email }, { auth: false }),
}