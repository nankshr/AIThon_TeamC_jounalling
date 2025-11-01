'use client';

import { useState } from 'react';
import { Search, X, AlertCircle, TrendingUp } from 'lucide-react';

interface SearchResult {
  id: string;
  text: string;
  date: string | null;
  relevance_score: number;
  full_text: string;
  entities: Record<string, unknown>;
  sentiment: { emotion: string; confidence: number } | null;
}

interface ContradictionResult {
  type: string;
  severity: 'high' | 'medium' | 'low';
  description: string;
  [key: string]: unknown;
}

export function SearchInterface() {
  const [activeTab, setActiveTab] = useState<'search' | 'contradictions' | 'insights'>(
    'search'
  );
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [contradictions, setContradictions] = useState<ContradictionResult[]>([]);
  const [selectedResult, setSelectedResult] = useState<SearchResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_k: 5 }),
      });

      const data = await response.json();

      if (data.success) {
        setSearchResults(data.results || []);
      } else {
        setError(data.error || 'Search failed');
      }
    } catch (err) {
      setError('Failed to perform search: ' + (err instanceof Error ? err.message : 'Unknown error'));
    } finally {
      setIsLoading(false);
    }
  };

  const handleDetectContradictions = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // This would need actual entries from the database
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/contradictions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ entries: [] }), // Would be populated with actual entries
      });

      const data = await response.json();

      if (data.success) {
        setContradictions(data.contradictions || []);
      } else {
        setError(data.error || 'Failed to detect contradictions');
      }
    } catch (err) {
      setError('Failed to detect contradictions: ' + (err instanceof Error ? err.message : 'Unknown error'));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-4 p-4">
      {/* Tab Navigation */}
      <div className="flex gap-2 border-b">
        <button
          onClick={() => setActiveTab('search')}
          className={`px-4 py-2 font-medium ${
            activeTab === 'search'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <Search className="inline w-4 h-4 mr-2" />
          Search
        </button>
        <button
          onClick={() => setActiveTab('contradictions')}
          className={`px-4 py-2 font-medium ${
            activeTab === 'contradictions'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <AlertCircle className="inline w-4 h-4 mr-2" />
          Issues
        </button>
        <button
          onClick={() => setActiveTab('insights')}
          className={`px-4 py-2 font-medium ${
            activeTab === 'insights'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <TrendingUp className="inline w-4 h-4 mr-2" />
          Insights
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          {error}
          <button
            onClick={() => setError(null)}
            className="ml-auto text-red-700 hover:text-red-900"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Search Tab */}
      {activeTab === 'search' && (
        <div className="space-y-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Search your journal entries... (e.g., 'vendors', 'budget', 'timeline')"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleSearch}
              disabled={isLoading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 font-medium"
            >
              {isLoading ? 'Searching...' : 'Search'}
            </button>
          </div>

          {/* Search Results */}
          <div className="space-y-2">
            {searchResults.length > 0 ? (
              <>
                <p className="text-sm text-gray-600 font-medium">
                  Found {searchResults.length} results
                </p>
                {searchResults.map((result) => (
                  <button
                    key={result.id}
                    onClick={() => setSelectedResult(result)}
                    className="w-full text-left p-3 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
                  >
                    <div className="flex justify-between items-start gap-2">
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900 line-clamp-2">
                          {result.text || result.full_text?.substring(0, 100)}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">{result.date}</p>
                      </div>
                      <span className="text-sm font-semibold text-blue-600 whitespace-nowrap">
                        {(result.relevance_score * 100).toFixed(0)}%
                      </span>
                    </div>
                  </button>
                ))}
              </>
            ) : (
              query && !isLoading && (
                <p className="text-center text-gray-500 py-8">No results found</p>
              )
            )}
          </div>

          {/* Selected Result Detail */}
          {selectedResult && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
              <div className="bg-white rounded-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto">
                <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-start">
                  <div>
                    <p className="text-sm text-gray-500">{selectedResult.date}</p>
                    <h3 className="text-lg font-bold text-gray-900">Entry Detail</h3>
                  </div>
                  <button
                    onClick={() => setSelectedResult(null)}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    <X className="w-6 h-6" />
                  </button>
                </div>
                <div className="p-4 space-y-4">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Content</h4>
                    <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                      {selectedResult.full_text}
                    </p>
                  </div>
                  {selectedResult.sentiment && (
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-2">Sentiment</h4>
                      <p className="text-gray-700">
                        {selectedResult.sentiment.emotion} (
                        {(selectedResult.sentiment.confidence * 100).toFixed(0)}% confidence)
                      </p>
                    </div>
                  )}
                  {selectedResult.entities && Object.keys(selectedResult.entities).length > 0 && (
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-2">Extracted Data</h4>
                      <pre className="bg-gray-50 p-3 rounded text-sm overflow-x-auto text-gray-700">
                        {JSON.stringify(selectedResult.entities, null, 2)}
                      </pre>
                    </div>
                  )}
                  <div className="flex gap-2">
                    <span className="text-sm text-gray-600 bg-gray-100 px-2 py-1 rounded">
                      Relevance: {(selectedResult.relevance_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Contradictions Tab */}
      {activeTab === 'contradictions' && (
        <div className="space-y-4">
          <button
            onClick={handleDetectContradictions}
            disabled={isLoading}
            className="w-full px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 disabled:bg-gray-400 font-medium"
          >
            {isLoading ? 'Detecting...' : 'Detect Contradictions'}
          </button>

          {contradictions.length > 0 && (
            <div className="space-y-2">
              {contradictions.map((contradiction, idx) => (
                <div
                  key={idx}
                  className={`p-4 rounded-lg border-l-4 ${
                    contradiction.severity === 'high'
                      ? 'bg-red-50 border-red-400'
                      : contradiction.severity === 'medium'
                        ? 'bg-amber-50 border-amber-400'
                        : 'bg-blue-50 border-blue-400'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <AlertCircle
                      className={`w-5 h-5 mt-0.5 ${
                        contradiction.severity === 'high'
                          ? 'text-red-600'
                          : contradiction.severity === 'medium'
                            ? 'text-amber-600'
                            : 'text-blue-600'
                      }`}
                    />
                    <div>
                      <p className="font-semibold text-gray-900">
                        {contradiction.type?.replace(/_/g, ' ').toUpperCase()}
                      </p>
                      <p className="text-gray-700 mt-1">{contradiction.description}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Insights Tab */}
      {activeTab === 'insights' && (
        <div className="p-4 text-center text-gray-500">
          <TrendingUp className="w-8 h-8 mx-auto mb-2 text-gray-400" />
          <p>Insights feature coming soon!</p>
          <p className="text-sm mt-1">Will show patterns, trends, and recommendations from your entries</p>
        </div>
      )}
    </div>
  );
}
