import { auth } from '@/auth'
import { Session } from 'next-auth'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public response?: Response
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

class ApiClient {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  private async getAuthHeaders(session?: Session | null): Promise<Record<string, string>> {
    // If session is provided, use it; otherwise get it from auth()
    const currentSession = session || await auth()
    
    if (!currentSession?.user) {
      throw new ApiError('No session found', 401)
    }
    // Extract JWT token from session
    const token = currentSession.token

    if (!token) {
      throw new ApiError('No access token found', 401)
    }

    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    }
  }

  async request<T>(
    endpoint: string,
    options: RequestInit & { session?: Session | null } = {}
  ): Promise<T> {
    const { session, ...requestOptions } = options
    const url = `${this.baseURL}${endpoint}`
    
    try {
      const headers = await this.getAuthHeaders(session)
      
      const response = await fetch(url, {
        ...requestOptions,
        headers: {
          ...headers,
          ...requestOptions.headers,
        },
      })

      if (response.status <= 200 || response.status >= 300) {
        console.log(`» Backend: ${requestOptions.method || 'GET'} ${url} \x1b[32m%s\x1b[0m`, `${response.status}`)
      }

      if (!response.ok) {
        const errorText = await response.text()
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`
        
        try {
          const errorJson = JSON.parse(errorText)
          errorMessage = errorJson.detail || errorMessage
        } catch {
          // If not JSON, use the raw text
          errorMessage = errorText || errorMessage
        }
        
        throw new ApiError(errorMessage, response.status, response)
      }

      const contentType = response.headers.get('content-type')
      if (contentType && contentType.includes('application/json')) {
        return await response.json()
      } else {
        return await response.text() as T
      }
    } catch (error) {
      if (error instanceof ApiError) {
        throw error
      }
      throw new ApiError(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`, 0)
    }
  }

  async get<T>(endpoint: string, session?: Session | null): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET', session })
  }

  async post<T>(endpoint: string, data?: any, session?: Session | null): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
      session,
    })
  }

  async put<T>(endpoint: string, data: any, session?: Session | null): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
      session,
    })
  }

  async delete<T>(endpoint: string, session?: Session | null): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE', session })
  }
}

export const apiClient = new ApiClient()