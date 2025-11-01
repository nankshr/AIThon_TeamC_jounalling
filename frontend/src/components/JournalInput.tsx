'use client'

import { useState } from 'react'
import { useStore } from '@/lib/store'
import { apiClient } from '@/lib/api'
import { Send } from 'lucide-react'

export default function JournalInput() {
  const [text, setText] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { addEntry, setError, suggestionMode } = useStore()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!text.trim()) {
      setError('Please enter some text')
      return
    }

    setIsSubmitting(true)
    try {
      const entry = await apiClient.createEntry(text, 'en', suggestionMode)
      addEntry(entry)
      setText('')
      setError(null)
    } catch (error: any) {
      setError(`Failed to create entry: ${error.message}`)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">New Journal Entry</h2>

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
