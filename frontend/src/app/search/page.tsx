'use client'

import { useState } from 'react'
import Header from '@/components/Header'
import { Search as SearchIcon, Loader, ChevronDown, ChevronUp } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Entity {
  [key: string]: any
}

interface Sentiment {
  emotion: string
  confidence: number
}

interface SearchResult {
  id: string
  text: string
  date: string | null
  relevance_score: number
  full_text: string
  entities: Entity
  sentiment: Sentiment | null
}

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)
  const [expandedId, setExpandedId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!query.trim()) {
      return
    }

    setIsSearching(true)
    setError(null)
    try {
      const response = await fetch(`${API_URL}/api/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query.trim(),
          top_k: 10,
        }),
      })

      if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`)
      }

      const data = await response.json()

      if (data.success) {
        setResults(data.results || [])
        console.log(`[Search] Found ${data.results?.length || 0} results`)
      } else {
        setError(data.error || 'Search failed')
        console.error('[Search] Error:', data.error)
      }

      setHasSearched(true)
    } catch (error: any) {
      console.error('[Search] Error:', error)
      setError(`Search failed: ${error.message}`)
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">🔍 Semantic Search</h1>
          <p className="text-gray-600 mb-6">Search your journal entries and explore related insights</p>

          <form onSubmit={handleSearch} className="flex gap-3">
            <div className="flex-1 relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch(e)}
                placeholder="Search entries... (e.g., 'vendors', 'budget concerns', 'timeline')"
                className="w-full px-4 py-3 pl-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>

            <button
              type="submit"
              disabled={isSearching || !query.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
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

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}
        </div>

        {/* Results */}
        <div>
          {!hasSearched && (
            <div className="bg-white rounded-xl shadow-md p-12 border border-gray-100 text-center">
              <div className="text-gray-400 mb-4 text-5xl">🔍</div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Search Your Entries</h3>
              <p className="text-gray-600">Use semantic search to find related entries and insights</p>
            </div>
          )}

          {error && hasSearched && (
            <div className="bg-white rounded-xl shadow-md p-12 border border-red-200 text-center">
              <div className="text-red-400 mb-4 text-5xl">⚠️</div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">Search Failed</h3>
              <p className="text-gray-600">{error}</p>
            </div>
          )}

          {hasSearched && results.length === 0 && !isSearching && !error && (
            <div className="bg-white rounded-xl shadow-md p-12 border border-gray-100 text-center">
              <div className="text-gray-400 mb-4 text-5xl">📭</div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">No Results Found</h3>
              <p className="text-gray-600">Try a different search term or check if you have any entries</p>
            </div>
          )}

          {results.length > 0 && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-sm p-4 border border-blue-200 bg-blue-50">
                <p className="text-sm text-blue-700">
                  ✨ <strong>Found {results.length} related entry{results.length !== 1 ? 'ies' : ''}</strong> ranked by semantic relevance
                </p>
              </div>

              <div className="space-y-4">
                {results.map((result) => (
                  <div
                    key={result.id}
                    className="bg-white rounded-xl shadow-md border border-gray-100 hover:shadow-lg transition-shadow overflow-hidden"
                  >
                    {/* Result Header */}
                    <button
                      onClick={() => setExpandedId(expandedId === result.id ? null : result.id)}
                      className="w-full p-6 text-left hover:bg-gray-50 transition-colors flex items-start justify-between"
                    >
                      <div className="flex-1 pr-4">
                        {/* Date and Relevance */}
                        <div className="flex items-center gap-3 mb-2">
                          <span className="text-xs text-gray-500">
                            📅 {result.date ? new Date(result.date).toLocaleDateString('en-IN', {
                              month: 'short',
                              day: 'numeric',
                              year: 'numeric'
                            }) : 'No date'}
                          </span>
                          <div className="h-1.5 bg-blue-100 rounded-full flex-1 max-w-xs overflow-hidden">
                            <div
                              className="h-full bg-blue-600 rounded-full"
                              style={{ width: `${Math.round(result.relevance_score * 100)}%` }}
                            />
                          </div>
                          <span className="text-sm font-bold text-blue-600">
                            {Math.round(result.relevance_score * 100)}% match
                          </span>
                        </div>

                        {/* Preview Text */}
                        <p className="text-gray-800 font-medium line-clamp-2 mb-3">
                          {result.text}
                        </p>

                        {/* Sentiment Badge */}
                        {result.sentiment && (
                          <div className="flex gap-2">
                            <span className={`text-xs px-3 py-1 rounded-full font-medium ${
                              result.sentiment.emotion === 'positive' ? 'bg-green-100 text-green-700' :
                              result.sentiment.emotion === 'negative' ? 'bg-red-100 text-red-700' :
                              'bg-gray-100 text-gray-700'
                            }`}>
                              💭 {result.sentiment.emotion}
                            </span>
                          </div>
                        )}
                      </div>

                      {/* Expand/Collapse Icon */}
                      <div className="text-gray-400">
                        {expandedId === result.id ? (
                          <ChevronUp className="w-5 h-5" />
                        ) : (
                          <ChevronDown className="w-5 h-5" />
                        )}
                      </div>
                    </button>

                    {/* Expanded Details */}
                    {expandedId === result.id && (
                      <div className="border-t border-gray-100 p-6 space-y-4 bg-gray-50">
                        {/* Full Text */}
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">📝 Full Entry</h4>
                          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                            {result.full_text}
                          </p>
                        </div>

                        {/* Sentiment Details */}
                        {result.sentiment && (
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-2">💭 Mood Analysis</h4>
                            <p className="text-gray-700">
                              <strong>{result.sentiment.emotion.charAt(0).toUpperCase() + result.sentiment.emotion.slice(1)}</strong> confidence: {Math.round(result.sentiment.confidence * 100)}%
                            </p>
                          </div>
                        )}

                        {/* Extracted Entities */}
                        {result.entities && Object.keys(result.entities).length > 0 && (
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-3">🔍 Extracted Information</h4>
                            <div className="space-y-2 text-sm">
                              {result.entities.vendors && result.entities.vendors.length > 0 && (
                                <p className="text-gray-700">
                                  <strong>🏢 Vendors:</strong> {Array.isArray(result.entities.vendors) ? result.entities.vendors.join(', ') : result.entities.vendors}
                                </p>
                              )}
                              {result.entities.costs && result.entities.costs.length > 0 && (
                                <p className="text-gray-700">
                                  <strong>💰 Budget:</strong> ₹{result.entities.costs.reduce((sum: number, c: any) => sum + (c.amount || 0), 0).toLocaleString('en-IN')}
                                </p>
                              )}
                              {result.entities.dates && result.entities.dates.length > 0 && (
                                <p className="text-gray-700">
                                  <strong>📅 Key Dates:</strong> {result.entities.dates.map((d: any) => {
                                    const dateStr = typeof d === 'string' ? d : d.date;
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

                        {/* Relevance Score */}
                        <div className="pt-2 border-t border-gray-200 text-xs text-gray-500">
                          Semantic relevance: {(result.relevance_score * 100).toFixed(1)}%
                        </div>
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
