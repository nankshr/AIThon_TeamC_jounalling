import { create } from 'zustand'

export interface JournalEntry {
  id: string
  raw_text: string
  language: string
  themes: string[]
  sentiment?: string
  created_at: string
  entities: any[]
  tasks: any[]
}

export interface Task {
  id: string
  action: string
  description?: string
  deadline?: string
  priority: string
  status: string
  completed_at?: string
  created_at: string
}

export interface UserPreference {
  id: string
  values: string[]
  budget_goal?: number
  wedding_date?: string
  primary_language: string
  suggestion_mode_default: boolean
  post_wedding_mode: boolean
  created_at: string
}

interface Store {
  // Journal state
  entries: JournalEntry[]
  currentEntry: JournalEntry | null
  setEntries: (entries: JournalEntry[]) => void
  setCurrentEntry: (entry: JournalEntry | null) => void
  addEntry: (entry: JournalEntry) => void

  // Task state
  tasks: Task[]
  setTasks: (tasks: Task[]) => void
  addTask: (task: Task) => void
  removeTask: (taskId: string) => void

  // User state
  userPreference: UserPreference | null
  setUserPreference: (preference: UserPreference) => void

  // UI state
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
  error: string | null
  setError: (error: string | null) => void
  suggestionMode: boolean
  setSuggestionMode: (mode: boolean) => void
}

export const useStore = create<Store>((set) => ({
  // Journal
  entries: [],
  currentEntry: null,
  setEntries: (entries) => set({ entries }),
  setCurrentEntry: (entry) => set({ currentEntry: entry }),
  addEntry: (entry) => set((state) => ({ entries: [entry, ...state.entries] })),

  // Tasks
  tasks: [],
  setTasks: (tasks) => set({ tasks }),
  addTask: (task) => set((state) => ({ tasks: [...state.tasks, task] })),
  removeTask: (taskId) => set((state) => ({
    tasks: state.tasks.filter((t) => t.id !== taskId),
  })),

  // User
  userPreference: null,
  setUserPreference: (preference) => set({ userPreference: preference }),

  // UI
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
  error: null,
  setError: (error) => set({ error }),
  suggestionMode: true,
  setSuggestionMode: (mode) => set({ suggestionMode: mode }),
}))
