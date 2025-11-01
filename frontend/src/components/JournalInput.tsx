'use client'

import { useState } from 'react'
import { useStore } from '@/lib/store'
import { apiClient } from '@/lib/api'
import { Send, Loader } from 'lucide-react'
import { VoiceRecorder } from './VoiceRecorder'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function JournalInput() {
  const [text, setText] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [extractedData, setExtractedData] = useState<any>(null)
  const [showSuggestions, setShowSuggestions] = useState(false)
  const { addEntry, setError, suggestionMode, addTask } = useStore()

  // First phase: Extract data from text (before Save Entry click)
  const handleExtractData = async () => {
    if (!text.trim()) {
      setError('Please enter some text')
      return
    }

    setIsProcessing(true)
    try {
      console.log('Sending journal entry to Intake Agent for processing...')
      const response = await fetch(`${API_URL}/api/journal/entries`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          language: 'en',
          transcribed_from_audio: false,
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to process entry')
      }

      const result = await response.json()
      console.log('Intake Agent result:', result)

      if (result.success && result.data) {
        console.log('Full extracted data:', result.data)
        setExtractedData(result.data)
        setShowSuggestions(true) // Keep suggestions visible
        console.log('Extracted entities:', result.data.entities)
        console.log('Extracted tasks:', result.data.tasks)
        console.log('Sentiment:', result.data.sentiment)
        console.log('Tasks count:', result.data.tasks?.explicit?.length || 0)
      }
    } catch (error: any) {
      console.error('Extraction error:', error)
      setError(`Failed to extract data: ${error.message}`)
    } finally {
      setIsProcessing(false)
    }
  }

  // Second phase: Save entry and tasks (after Save Entry click)
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!text.trim()) {
      setError('Please enter some text')
      return
    }

    setIsSubmitting(true)
    try {
      // Save the journal entry first
      const entry = await apiClient.createEntry(text, 'en', suggestionMode)
      addEntry(entry)
      console.log('[Entry] Created entry:', entry.id)

      // Get checked tasks from the UI and create them
      let tasksCreated = 0
      if (extractedData?.tasks?.explicit?.length > 0) {
        const allTasks = extractedData.tasks.explicit
        const checkedTasks: any[] = []

        // Check which tasks are selected
        allTasks.forEach((task: any, idx: number) => {
          const checkbox = document.getElementById(`task-${idx}`) as HTMLInputElement
          if (checkbox?.checked) {
            checkedTasks.push(task)
          }
        })

        console.log('[Tasks] Found', checkedTasks.length, 'checked tasks out of', allTasks.length)

        // Create task entries in the database
        if (checkedTasks.length > 0) {
          console.log('[Tasks] Creating tasks:', checkedTasks.map((t: any) => t.title || t.task))

          for (const task of checkedTasks) {
            try {
              // Handle both task.title and task.task fields from API
              const taskTitle = task.title || task.task || 'Untitled Task'
              console.log('[Tasks] Creating task:', taskTitle)
              console.log('[Tasks] Full task object:', task)

              const taskPayload = {
                action: taskTitle,
                description: task.description || '',
                priority: task.priority || 'medium',
                deadline: task.deadline || null,
              }
              console.log('[Tasks] Task payload:', taskPayload)

              const response = await fetch(`${API_URL}/api/tasks`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(taskPayload),
              })

              console.log('[Tasks] Response status:', response.status)

              if (!response.ok) {
                const errorData = await response.json()
                console.error('[Tasks] Failed to create task:', taskTitle, response.status, errorData)
                throw new Error(`Failed to create task: ${errorData.detail || response.statusText}`)
              }

              const createdTask = await response.json()
              console.log('[Tasks] Successfully created task:', taskTitle, createdTask)
              // Update store so task appears immediately in TaskPanel
              addTask(createdTask)
              tasksCreated++
            } catch (err: any) {
              console.error('[Tasks] Error creating task:', task.task || task.title, err)
              // Continue creating other tasks even if one fails
            }
          }

          if (tasksCreated > 0) {
            console.log(`[Tasks] Successfully created ${tasksCreated} tasks`)
            setError(`Created entry and ${tasksCreated} task(s)!`)
          } else {
            console.log('[Tasks] No tasks were successfully created')
            setError('Created entry but no tasks were saved')
          }
        } else {
          console.log('[Tasks] No tasks were checked')
          setError('Created entry (no tasks selected)')
        }
      } else {
        console.log('[Tasks] No tasks in extracted data')
        setError('Entry saved successfully!')
      }

      // Clear form and suggestions after successful save
      setText('')
      setExtractedData(null)
      setShowSuggestions(false)

      // Show success message briefly then clear it
      setTimeout(() => {
        setError(null)
      }, 3000)
    } catch (error: any) {
      console.error('Entry save error:', error)
      setError(`Failed to save entry: ${error.message}`)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleTranscriptionComplete = (transcribedText: string, language: string) => {
    setText(transcribedText)
    setError(null)
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">New Journal Entry</h2>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Record voice or type
        </label>
        <VoiceRecorder
          onTranscriptionComplete={handleTranscriptionComplete}
          isLoading={isSubmitting}
        />
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="journal-text" className="block text-sm font-medium text-gray-700 mb-2">
            What's on your mind?
          </label>
          <textarea
            id="journal-text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Share your thoughts about the wedding planning..."
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
            rows={5}
            disabled={isSubmitting}
          />
        </div>

        {/* Processing indicator */}
        {isProcessing && (
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg flex items-center gap-2">
            <Loader className="w-4 h-4 animate-spin text-blue-600" />
            <span className="text-sm text-blue-700">Processing with AI...</span>
          </div>
        )}

        {/* Get AI Suggestions Button */}
        {text.trim() && !showSuggestions && !isProcessing && (
          <button
            type="button"
            onClick={handleExtractData}
            disabled={isSubmitting || isProcessing}
            className="w-full px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-300 font-medium rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span>✨ Get AI Suggestions</span>
          </button>
        )}

        {/* Extracted data display - PERSISTENT */}
        {showSuggestions && extractedData && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <h3 className="text-sm font-semibold text-green-900 mb-3">✓ AI Analysis</h3>

            {/* Summary Stats */}
            <div className="grid grid-cols-2 gap-3 text-xs mb-4">
              {extractedData.entities?.vendors?.length > 0 && (
                <div>
                  <p className="font-medium text-green-800">Vendors Found</p>
                  <p className="text-green-700">{extractedData.entities.vendors.length}</p>
                </div>
              )}
              {extractedData.tasks?.explicit?.length > 0 && (
                <div>
                  <p className="font-medium text-green-800">Tasks Identified</p>
                  <p className="text-green-700">{extractedData.tasks.explicit.length}</p>
                </div>
              )}
              {extractedData.sentiment && (
                <div>
                  <p className="font-medium text-green-800">Mood</p>
                  <p className="text-green-700 capitalize">{extractedData.sentiment.emotion}</p>
                </div>
              )}
              {extractedData.timeline && (
                <div>
                  <p className="font-medium text-green-800">Timeline</p>
                  <p className="text-green-700 capitalize">{extractedData.timeline}</p>
                </div>
              )}
            </div>

            {/* Suggested Tasks - WITH FULL DETAILS */}
            {extractedData.tasks?.explicit && extractedData.tasks.explicit.length > 0 ? (
              <div className="bg-white rounded p-4 border-2 border-green-300 mt-4">
                <p className="text-sm font-bold text-green-900 mb-4">✓ Suggested Tasks ({extractedData.tasks.explicit.length}):</p>
                <div className="space-y-3">
                  {extractedData.tasks.explicit.map((task: any, idx: number) => (
                    <div key={idx} className="p-3 bg-gradient-to-r from-green-50 to-white rounded-lg border-2 border-green-200 hover:border-green-400 transition-all">
                      <div className="flex items-start gap-3">
                        <input
                          type="checkbox"
                          defaultChecked
                          className="mt-1 cursor-pointer w-4 h-4"
                          id={`task-${idx}`}
                        />
                        <div className="flex-1 cursor-pointer" onClick={() => {
                          const checkbox = document.getElementById(`task-${idx}`) as HTMLInputElement
                          if (checkbox) checkbox.checked = !checkbox.checked
                        }}>
                          <div className="flex items-baseline gap-2 mb-1">
                            <span className="text-sm font-bold text-green-900">{task.title || task.task || 'Task'}</span>
                            {task.priority && (
                              <span className={`text-xs font-bold px-2 py-1 rounded-full ${
                                task.priority === 'high' ? 'bg-red-200 text-red-800' :
                                task.priority === 'medium' ? 'bg-amber-200 text-amber-800' :
                                'bg-blue-200 text-blue-800'
                              }`}>
                                [{task.priority.toUpperCase()}]
                              </span>
                            )}
                          </div>
                          {task.description && (
                            <p className="text-xs text-gray-700 mt-1 pl-1">{task.description}</p>
                          )}
                          <div className="flex gap-3 mt-2 text-xs text-gray-600">
                            {task.deadline && (
                              <span className="flex items-center gap-1">📅 <strong>Due:</strong> {new Date(task.deadline).toLocaleDateString('en-IN')}</span>
                            )}
                            {task.status && (
                              <span className="flex items-center gap-1">📌 <strong>Status:</strong> {task.status}</span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : null}

            {/* Suggested Entities */}
            {(extractedData.entities?.vendors?.length > 0 ||
              extractedData.entities?.costs?.length > 0 ||
              extractedData.entities?.dates?.length > 0) && (
              <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-sm font-bold text-blue-900 mb-3">📋 Extracted Information:</p>
                <div className="space-y-2 text-xs">
                  {extractedData.entities?.vendors?.length > 0 && (
                    <p className="text-blue-800">
                      <strong>🏢 Vendors:</strong> {extractedData.entities.vendors.map((v: any) => {
                        if (typeof v === 'string') return v;
                        if (v && typeof v === 'object') {
                          return v.name || v.vendor || v.title || JSON.stringify(v);
                        }
                        return String(v);
                      }).join(', ')}
                    </p>
                  )}
                  {extractedData.entities?.costs?.length > 0 && (
                    <p className="text-blue-800">
                      <strong>💰 Total Budget:</strong> ₹{extractedData.entities.costs.reduce((sum: number, c: any) => sum + (c.amount || 0), 0).toLocaleString('en-IN')}
                    </p>
                  )}
                  {extractedData.entities?.dates?.length > 0 && (
                    <p className="text-blue-800">
                      <strong>📅 Important Dates:</strong> {extractedData.entities.dates.map((d: any) => {
                        const dateStr = d.date || d;
                        try {
                          return new Date(dateStr).toLocaleDateString('en-IN');
                        } catch {
                          return dateStr;
                        }
                      }).join(', ')}
                    </p>
                  )}
                </div>
              </div>
            )}

            {/* Change Button */}
            <button
              type="button"
              onClick={() => setShowSuggestions(false)}
              className="mt-3 text-xs text-green-600 hover:text-green-800 font-medium"
            >
              Dismiss suggestions
            </button>
          </div>
        )}

        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-600">
            {suggestionMode ? (
              <span className="text-green-600">✓ AI suggestions enabled</span>
            ) : (
              <span className="text-gray-500">AI suggestions disabled</span>
            )}
          </div>

          <button
            type="submit"
            disabled={isSubmitting || !text.trim()}
            className="bg-primary hover:bg-primary/90 text-white font-medium py-2 px-6 rounded-lg flex items-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
            {isSubmitting ? 'Saving...' : 'Save Entry'}
          </button>
        </div>
      </form>
    </div>
  )
}
