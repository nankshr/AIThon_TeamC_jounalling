'use client'

import { useState, useEffect } from 'react'
import { useStore } from '@/lib/store'
import { apiClient } from '@/lib/api'
import JournalInput from '@/components/JournalInput'
import JournalList from '@/components/JournalList'
import TaskPanel from '@/components/TaskPanel'
import Header from '@/components/Header'

export default function Home() {
  const [isInitialized, setIsInitialized] = useState(false)
  const { setEntries, setTasks, setUserPreference, setError } = useStore()

  useEffect(() => {
    const initialize = async () => {
      try {
        // Check health
        await apiClient.healthCheck()

        // Load user preferences
        const userPref = await apiClient.getUserPreferences()
        setUserPreference(userPref)

        // Load entries
        const entriesData = await apiClient.getEntries()
        setEntries(entriesData.entries || [])

        // Load pending tasks
        const tasksData = await apiClient.getPendingTasks()
        setTasks(tasksData.tasks || [])

        setIsInitialized(true)
      } catch (error: any) {
        console.error('Initialization error:', error)
        setError(`Failed to connect to API: ${error.message}`)
      }
    }

    initialize()
  }, [setEntries, setTasks, setUserPreference, setError])

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <Header />

      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main content - Journal input and entries */}
          <div className="lg:col-span-2 space-y-8">
            {/* Journal Input */}
            <JournalInput />

            {/* Recent Entries */}
            {isInitialized && <JournalList />}
          </div>

          {/* Sidebar - Tasks and timeline */}
          <div className="lg:col-span-1">
            {isInitialized && <TaskPanel />}
          </div>
        </div>
      </div>
    </main>
  )
}
