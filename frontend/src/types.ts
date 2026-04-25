export interface User {
  id: number
  email: string
  is_active: boolean
}

export interface AuthToken {
  access_token: string
  token_type: string
}

export interface PIIData {
  first_name: string
  last_name: string
  email?: string
  phone?: string
  address?: string
  city?: string
  state?: string
  zip_code?: string
}

export interface SearchSource {
  source_name: string
  source_url?: string
  data_found: boolean
  data_details?: string
}

export interface SearchResult {
  id: number
  first_name: string
  last_name: string
  email?: string
  phone?: string
  address?: string
  created_at: string
  sources: SearchSource[]
}

export interface SearchHistoryItem {
  id: number
  first_name: string
  last_name: string
  created_at: string
  result_count: number
}