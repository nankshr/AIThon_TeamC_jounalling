'use client'

import { useStore } from '@/lib/store'
import { Calendar, Tag } from 'lucide-react'

export default function JournalList() {
  const { entries } = useStore()

  if (entries.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md p-12 border border-gray-100 text-center">
        <div className="text-gray-400 mb-4 text-4xl">📝</div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">No entries yet</h3>
        <p className="text-gray-600">Start journaling to see your entries here</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-900">Recent Entries</h2>

      <div className="space-y-4">
        {entries.map((entry) => (
          <div
            key={entry.id}
            className="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-2 text-gray-600 text-sm">
                <Calendar className="w-4 h-4" />
                {new Date(entry.created_at).toLocaleDateString('en-US', {
                  weekday: 'short',
                  month: 'short',
                  day: 'numeric',
                })}
              </div>

              {entry.sentiment && (
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                  {entry.sentiment}
                </span>
              )}
            </div>

            <p className="text-gray-800 mb-4 line-clamp-3">{entry.raw_text}</p>

            {entry.themes.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-3">
                {entry.themes.slice(0, 3).map((theme) => (
                  <span
                    key={theme}
                    className="flex items-center gap-1 text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full"
                  >
                    <Tag className="w-3 h-3" />
                    {theme}
                  </span>
                ))}
                {entry.themes.length > 3 && (
                  <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full">
                    +{entry.themes.length - 3} more
                  </span>
                )}
              </div>
            )}

            {entry.entities.length > 0 && (
              <div className="pt-3 border-t border-gray-100">
                <p className="text-xs text-gray-600 mb-2">
                  Extracted: {entry.entities.length} items
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
