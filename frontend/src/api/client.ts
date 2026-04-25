import axios from 'axios'
import type { AuthToken, User, PIIData, SearchResult, SearchHistoryItem } from '../types'

const api = axios.create({
  baseURL: '/auth',
  headers: { 'Content-Type': 'application/json' },
})

export function setAuthToken(token: string | null) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    localStorage.setItem('token', token)
  } else {
    delete api.defaults.headers.common['Authorization']
    localStorage.removeItem('token')
  }
}

export function getStoredToken(): string | null {
  return localStorage.getItem('token')
}

export async function register(email: string, password: string): Promise<User> {
  const response = await api.post<User>('/register', { email, password })
  return response.data
}

export async function login(email: string, password: string): Promise<AuthToken> {
  console.log('Attempting login for:', email)
  const response = await api.post<AuthToken>(
    '/login',
    new URLSearchParams({ username: email, password }).toString(),
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  )
  console.log('Login response:', response.data)
  setAuthToken(response.data.access_token)
  return response.data
}

export async function getCurrentUser(): Promise<User> {
  const response = await api.get<User>('/me')
  return response.data
}

const piiApi = axios.create({
  baseURL: '/pii',
  headers: { 'Content-Type': 'application/json' },
})

piiApi.interceptors.request.use((config) => {
  const token = getStoredToken()
  if (token) {
    config.headers.common['Authorization'] = `Bearer ${token}`
  }
  return config
})

export async function submitScan(data: PIIData): Promise<SearchResult> {
  const response = await piiApi.post<SearchResult>('/scan', data)
  return response.data
}

export async function getSearches(): Promise<SearchHistoryItem[]> {
  const response = await piiApi.get<SearchHistoryItem[]>('/searches')
  return response.data
}

export async function getSearchResult(id: number): Promise<SearchResult> {
  const response = await piiApi.get<SearchResult>(`/searches/${id}`)
  return response.data
}