import axios from 'axios'
import type { AuthToken, User, PIIData, SearchResult, SearchHistoryItem } from '../types'

const api = axios.create({
  baseURL: '/auth',
  headers: { 'Content-Type': 'application/json' },
})

const piiApi = axios.create({
  baseURL: '/pii',
  headers: { 'Content-Type': 'application/json' },
})

export function setAuthToken(token: string | null) {
  if (token) {
    localStorage.setItem('token', token)
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    piiApi.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    localStorage.removeItem('token')
    delete api.defaults.headers.common['Authorization']
    delete piiApi.defaults.headers.common['Authorization']
  }
}

export function getStoredToken(): string | null {
  return localStorage.getItem('token')
}

export function initApiToken() {
  const token = getStoredToken()
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    piiApi.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
}

initApiToken()

export async function register(email: string, password: string): Promise<User> {
  const response = await api.post<User>('register', { email, password })
  return response.data
}

export async function login(email: string, password: string): Promise<AuthToken> {
  const params = new URLSearchParams({ username: email, password }).toString()
  const response = await api.post<AuthToken>(
    'login',
    params,
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  )
  setAuthToken(response.data.access_token)
  return response.data
}

export async function getCurrentUser(): Promise<User> {
  const response = await api.get<User>('me')
  return response.data
}

export async function submitScan(data: PIIData): Promise<SearchResult> {
  const response = await piiApi.post<SearchResult>('scan', data)
  return response.data
}

export async function getSearches(): Promise<SearchHistoryItem[]> {
  const response = await piiApi.get<SearchHistoryItem[]>('searches')
  return response.data
}

export async function getSearchResult(id: number): Promise<SearchResult> {
  const response = await piiApi.get<SearchResult>(`searches/${id}`)
  return response.data
}