'use client'

import { useState } from 'react'
import { apiClient } from '@/lib/api'
import Header from '@/components/Header'
import { Search as SearchIcon, Loader } from 'lucide-react'

interface SearchResult {
  id: string
  raw_text: string
  created_at: string
  themes: string[]
}

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!query.trim()) {
      return
    }

    setIsSearching(true)
    try {
      const response = await apiClient.searchJournal(query, 20, 'hybrid')
      setResults(response.results || [])
      setHasSearched(true)
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <Header />

      <div className="container mx-auto px-4 py-12 max-w-4xl">
        {/* Search Form */}
        <div className="bg-white rounded-xl shadow-md p-8 border border-gray-100 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Search Journal</h1>
          <p className="text-gray-600 mb-6">Find entries by keywords or topics</p>

          <form onSubmit={handleSearch} className="flex gap-3">
            <div className="flex-1 relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search your journal entries..."
                className="w-full px-4 py-3 pl-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              />
              <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>

            <button
              type="submit"
              disabled={isSearching || !query.trim()}
              className="bg-primary hover:bg-primary/90 text-white font-medium py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isSearching ? (
                <>
                  <Loader className="w-4 h-4 animate-spin" />
                  Searching...
                </>
              ) : (
                <>
                  <SearchIcon className="w-4 h-4" />
                  Search
                </>
              )}
            </button>
          </form>
        </div>

        {/* Results */}
        <div>
          {!hasSearched && (
            <div className="bg-white rounded-xl shadow-md p-12 border border-gray-100 text-center">
              <div className="text-gray-400 mb-4 text-4xl">🔍</div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">No searches yet</h3>
              <p className="text-gray-600">Try searching for a topic or keyword</p>
            </div>
          )}

          {hasSearched && results.length === 0 && !isSearching && (
            <div className="bg-white rounded-xl shadow-md p-12 border border-gray-100 text-center">
              <div className="text-gray-400 mb-4 text-4xl">📭</div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">No results found</h3>
              <p className="text-gray-600">Try a different search term</p>
            </div>
          )}

          {results.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-xl font-bold text-gray-900">
                Found {results.length} result{results.length !== 1 ? 's' : ''}
              </h2>

              <div className="space-y-4">
                {results.map((result) => (
                  <div
                    key={result.id}
                    className="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow"
                  >
                    <div className="text-sm text-gray-600 mb-3">
                      {new Date(result.created_at).toLocaleDateString('en-US', {
                        weekday: 'short',
                        month: 'short',
                        day: 'numeric',
                        hour: 'numeric',
                        minute: 'numeric',
                      })}
                    </div>

                    <p className="text-gray-800 mb-3">{result.raw_text}</p>

                    {result.themes.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {result.themes.map((theme) => (
                          <span
                            key={theme}
                            className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full"
                          >
                            {theme}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
