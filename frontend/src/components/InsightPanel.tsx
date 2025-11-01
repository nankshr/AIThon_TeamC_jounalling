'use client';

import { useState } from 'react';
import { AlertCircle, TrendingUp, Lightbulb, CheckCircle, X } from 'lucide-react';

interface Insight {
  patterns: Array<{
    type: string;
    theme?: string;
    frequency?: number;
    description: string;
  }>;
  recommendations: Array<{
    type: string;
    message: string;
    area?: string;
    amount?: number;
  }>;
  alerts: Array<{
    type: string;
    severity: 'high' | 'medium' | 'low';
    message: string;
    recommendation?: string;
  }>;
  sentiment_trend?: {
    dominant_emotion: string;
    count: number;
    trend_description: string;
  };
  budget_status?: {
    total_spent: number;
    by_category: Record<string, number>;
    largest_category: string;
    largest_amount: number;
  };
  task_summary?: {
    total_tasks: number;
    completed: number;
    pending: number;
    completion_rate: number;
    high_priority: number;
  };
}

interface NextStep {
  priority: 'high' | 'medium' | 'low';
  action: string;
  deadline?: string;
  reason?: string;
}

export function InsightPanel() {
  const [insights, setInsights] = useState<Insight | null>(null);
  const [nextSteps, setNextSteps] = useState<NextStep[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dismissedAlerts, setDismissedAlerts] = useState<Set<number>>(new Set());

  const handleGenerateInsights = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // This would be called with actual entries from the database
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/insights`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ entries: [] }), // Would be populated with actual entries
      });

      const data = await response.json();

      if (data.success) {
        setInsights(data.insights);
        await handleGetNextSteps();
      } else {
        setError(data.error || 'Failed to generate insights');
      }
    } catch (err) {
      setError('Failed to generate insights: ' + (err instanceof Error ? err.message : 'Unknown error'));
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetNextSteps = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/next-steps`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ entries: [] }), // Would be populated with actual entries
      });

      const data = await response.json();

      if (data.success) {
        setNextSteps(data.next_steps || []);
      }
    } catch (err) {
      console.error('Failed to get next steps:', err);
    }
  };

  const dismissAlert = (index: number) => {
    setDismissedAlerts((prev) => new Set([...prev, index]));
  };

  if (!insights) {
    return (
      <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-6 text-center">
        <Lightbulb className="w-12 h-12 text-blue-600 mx-auto mb-3" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Wedding Insights</h3>
        <p className="text-gray-600 mb-4">
          Get AI-powered recommendations based on your journal entries
        </p>
        <button
          onClick={handleGenerateInsights}
          disabled={isLoading}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 font-medium"
        >
          {isLoading ? 'Generating...' : 'Generate Insights'}
        </button>
        {error && <p className="text-red-600 text-sm mt-3">{error}</p>}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Alerts Section */}
      {insights.alerts && insights.alerts.length > 0 && (
        <div className="space-y-2">
          <h3 className="font-semibold text-gray-900 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-600" />
            Alerts ({insights.alerts.length})
          </h3>
          {insights.alerts.map((alert, idx) => (
            !dismissedAlerts.has(idx) && (
              <div
                key={idx}
                className={`p-3 rounded-lg border-l-4 ${
                  alert.severity === 'high'
                    ? 'bg-red-50 border-red-400'
                    : alert.severity === 'medium'
                      ? 'bg-amber-50 border-amber-400'
                      : 'bg-blue-50 border-blue-400'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1">
                    <p
                      className={`font-medium ${
                        alert.severity === 'high'
                          ? 'text-red-900'
                          : alert.severity === 'medium'
                            ? 'text-amber-900'
                            : 'text-blue-900'
                      }`}
                    >
                      {alert.message}
                    </p>
                    {alert.recommendation && (
                      <p className="text-sm text-gray-700 mt-1">Tip: {alert.recommendation}</p>
                    )}
                  </div>
                  <button
                    onClick={() => dismissAlert(idx)}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )
          ))}
        </div>
      )}

      {/* Sentiment Trend */}
      {insights.sentiment_trend && (
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 flex items-center gap-2 mb-2">
            <TrendingUp className="w-5 h-5 text-purple-600" />
            Emotion Trend
          </h4>
          <p className="text-gray-700">
            <span className="font-semibold capitalize">{insights.sentiment_trend.dominant_emotion}</span>
            {' '}
            ({insights.sentiment_trend.count} entries)
          </p>
          <p className="text-sm text-gray-600 mt-1">{insights.sentiment_trend.trend_description}</p>
        </div>
      )}

      {/* Budget Status */}
      {insights.budget_status && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-2">Budget Status</h4>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-gray-700">Total Spent:</span>
              <span className="font-semibold text-gray-900">
                ${insights.budget_status.total_spent.toLocaleString()}
              </span>
            </div>
            {insights.budget_status.largest_category && (
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-600">Largest category:</span>
                <span className="text-gray-900">
                  {insights.budget_status.largest_category} (${insights.budget_status.largest_amount.toLocaleString()})
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Task Summary */}
      {insights.task_summary && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-2">Task Summary</h4>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <p className="text-sm text-gray-600">Total Tasks</p>
              <p className="text-2xl font-bold text-blue-600">{insights.task_summary.total_tasks}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Completion Rate</p>
              <p className="text-2xl font-bold text-green-600">
                {insights.task_summary.completion_rate.toFixed(0)}%
              </p>
            </div>
          </div>
          <div className="mt-3 text-sm text-gray-700">
            <p>High Priority: {insights.task_summary.high_priority}</p>
            <p>Pending: {insights.task_summary.pending}</p>
          </div>
        </div>
      )}

      {/* Recommendations */}
      {insights.recommendations && insights.recommendations.length > 0 && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 flex items-center gap-2 mb-3">
            <Lightbulb className="w-5 h-5 text-indigo-600" />
            Recommendations ({insights.recommendations.length})
          </h4>
          <ul className="space-y-2">
            {insights.recommendations.map((rec, idx) => (
              <li key={idx} className="flex gap-2 text-sm">
                <CheckCircle className="w-4 h-4 text-indigo-600 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700">{rec.message}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Patterns */}
      {insights.patterns && insights.patterns.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-3">Patterns Found</h4>
          <ul className="space-y-2">
            {insights.patterns.map((pattern, idx) => (
              <li key={idx} className="text-sm text-gray-700">
                <span className="font-medium">{pattern.description}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Next Steps */}
      {nextSteps.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-3">Next Steps</h4>
          <ul className="space-y-2">
            {nextSteps.slice(0, 5).map((step, idx) => (
              <li
                key={idx}
                className={`p-2 rounded border-l-4 ${
                  step.priority === 'high'
                    ? 'bg-red-50 border-red-400'
                    : step.priority === 'medium'
                      ? 'bg-amber-50 border-amber-400'
                      : 'bg-gray-50 border-gray-400'
                }`}
              >
                <p className="font-medium text-gray-900">{step.action}</p>
                {step.deadline && <p className="text-sm text-gray-600">Due: {step.deadline}</p>}
                {step.reason && <p className="text-sm text-gray-600">{step.reason}</p>}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Refresh Button */}
      <button
        onClick={handleGenerateInsights}
        disabled={isLoading}
        className="w-full px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:bg-gray-400 font-medium text-sm"
      >
        {isLoading ? 'Refreshing...' : 'Refresh Insights'}
      </button>
    </div>
  );
}
