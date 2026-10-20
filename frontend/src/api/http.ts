const BASE = import.meta.env.VITE_API_URL ?? '/api'

export class ApiError extends Error {
    constructor(public status: number, message: string, public errors?: Record<string, string[]>) {
        super(message)
    }
}

interface RequestOptions extends Omit<RequestInit, 'body'> {
    body?: unknown
    auth?: boolean
    responseType?: 'json' | 'blob'
}

export async function http<T>(path: string, options: RequestOptions = {}): Promise<T> {
    const {body, auth = true, headers, responseType = 'json', ...rest} = options
    const token = localStorage.getItem('token')

    const isFormData = body instanceof FormData

    let requestBody: BodyInit | undefined
    if (body === undefined) {
        requestBody = undefined
    } else if (isFormData) {
        requestBody = body
    } else {
        requestBody = JSON.stringify(body)
    }

    const defaultHeaders: Record<string, string> = {
        Accept: responseType === 'blob' ? '*/*' : 'application/json',
    }

    if (body !== undefined && !isFormData) {
        defaultHeaders['Content-Type'] = 'application/json'
    }

    const response = await fetch(`${BASE}${path}`, {
        ...rest,
        headers: {
            ...defaultHeaders,
            ...(auth && token ? {Authorization: `Bearer ${token}`} : {}),
            ...headers,
        },
        body: requestBody,
    })

    if (response.status === 401 && auth) {
        localStorage.removeItem('token')
        window.dispatchEvent(new Event('auth:logout'))
    }
    if (!response.ok) {
        const payload = await response.json().catch(() => ({}))
        throw new ApiError(
            response.status,
            payload.message ?? payload.detail ?? 'Une erreur est survenue',
            payload.errors,
        )
    }
    if (response.status === 204) return undefined as T
    if (responseType === 'blob') return response.blob() as Promise<T>
    return response.json()
}

export const api = {
    get: <T>(path: string, opts?: RequestOptions) => http<T>(path, {...opts, method: 'GET'}),
    post: <T>(path: string, body?: unknown, opts?: RequestOptions) => http<T>(path, {...opts, method: 'POST', body}),
    put: <T>(path: string, body?: unknown, opts?: RequestOptions) => http<T>(path, {...opts, method: 'PUT', body}),
    patch: <T>(path: string, body?: unknown, opts?: RequestOptions) => http<T>(path, {...opts, method: 'PATCH', body}),
    delete: <T>(path: string, opts?: RequestOptions) => http<T>(path, {...opts, method: 'DELETE'}),
}
