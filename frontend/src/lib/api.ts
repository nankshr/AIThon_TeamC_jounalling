import axios, { AxiosInstance } from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiClient {
  private client: AxiosInstance

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }

  // Journal endpoints
  async createEntry(text: string, language: string = 'en', suggestion_mode: boolean = true) {
    const response = await this.client.post('/api/journal/entry', {
      text,
      language,
      suggestion_mode,
    })
    return response.data
  }

  async getEntries(limit: number = 50, offset: number = 0) {
    const response = await this.client.get('/api/journal/entries', {
      params: { limit, offset },
    })
    return response.data
  }

  async getEntry(entryId: string) {
    const response = await this.client.get(`/api/journal/entry/${entryId}`)
    return response.data
  }

  async searchJournal(query: string, limit: number = 10, search_type: string = 'hybrid') {
    const response = await this.client.post('/api/journal/search', {
      query,
      limit,
      search_type,
    })
    return response.data
  }

  // Task endpoints
  async createTask(action: string, description?: string, deadline?: string, priority: string = 'medium') {
    const response = await this.client.post('/api/tasks', {
      action,
      description,
      deadline,
      priority,
    })
    return response.data
  }

  async getPendingTasks() {
    const response = await this.client.get('/api/tasks/pending')
    return response.data
  }

  async completeTask(taskId: string) {
    const response = await this.client.post(`/api/tasks/${taskId}/complete`)
    return response.data
  }

  async getTaskHistory(limit: number = 50) {
    const response = await this.client.get('/api/tasks/history', {
      params: { limit },
    })
    return response.data
  }

  // User endpoints
  async getUserPreferences() {
    const response = await this.client.get('/api/user/preferences')
    return response.data
  }

  async updateUserPreferences(preferences: any) {
    const response = await this.client.put('/api/user/preferences', preferences)
    return response.data
  }

  async getTimelineStatus() {
    const response = await this.client.get('/api/user/timeline')
    return response.data
  }

  // Health check
  async healthCheck() {
    const response = await this.client.get('/health')
    return response.data
  }
}

export const apiClient = new ApiClient(API_URL)
