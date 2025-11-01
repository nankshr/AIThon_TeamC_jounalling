'use client';

import { useState, useEffect } from 'react';
import { Calendar, DollarSign, CheckCircle, Users, TrendingUp, AlertCircle } from 'lucide-react';

interface DashboardStats {
  totalEntries: number;
  completedTasks: number;
  pendingTasks: number;
  totalSpent: number;
  budgetGoal: number;
  daysToWedding: number;
  lastEntryDate: string | null;
  sentimentTrend: string;
}

export function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // In a real app, this would fetch from the API
    // For now, we'll show a placeholder
    setStats({
      totalEntries: 0,
      completedTasks: 0,
      pendingTasks: 0,
      totalSpent: 0,
      budgetGoal: 0,
      daysToWedding: 0,
      lastEntryDate: null,
      sentimentTrend: 'neutral',
    });
    setIsLoading(false);
  }, []);

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="bg-gray-200 rounded-lg h-32 animate-pulse" />
        ))}
      </div>
    );
  }

  const budgetPercent = stats?.budgetGoal
    ? ((stats.totalSpent / stats.budgetGoal) * 100).toFixed(0)
    : 0;
  const taskCompletionPercent =
    (stats?.completedTasks || 0) + (stats?.pendingTasks || 0) > 0
      ? (
          ((stats?.completedTasks || 0) /
            ((stats?.completedTasks || 0) + (stats?.pendingTasks || 0))) *
          100
        ).toFixed(0)
      : 0;

  const isOverBudget = (stats?.totalSpent || 0) > (stats?.budgetGoal || 0);
  const isTimePressure = (stats?.daysToWedding || 100) < 30;

  return (
    <div className="space-y-6">
      {/* Critical Alerts */}
      <div className="space-y-2">
        {isOverBudget && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-red-900">Budget Alert</p>
              <p className="text-sm text-red-700">
                You've spent ${stats?.totalSpent} of your ${stats?.budgetGoal} budget
              </p>
            </div>
          </div>
        )}
        {isTimePressure && (
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-amber-900">Timeline Alert</p>
              <p className="text-sm text-amber-700">
                Only {stats?.daysToWedding} days left! {stats?.pendingTasks} tasks pending
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Journal Entries */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-gray-900">Journal Entries</h3>
            <Users className="w-5 h-5 text-blue-600" />
          </div>
          <p className="text-3xl font-bold text-blue-600">{stats?.totalEntries || 0}</p>
          <p className="text-sm text-gray-600 mt-1">
            {stats?.lastEntryDate ? `Last entry: ${stats.lastEntryDate}` : 'No entries yet'}
          </p>
        </div>

        {/* Tasks Progress */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-gray-900">Tasks</h3>
            <CheckCircle className="w-5 h-5 text-green-600" />
          </div>
          <div className="flex items-end gap-2">
            <p className="text-3xl font-bold text-green-600">{stats?.completedTasks || 0}</p>
            <p className="text-gray-600">of {(stats?.completedTasks || 0) + (stats?.pendingTasks || 0)}</p>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
            <div
              className="bg-green-600 h-2 rounded-full transition-all"
              style={{ width: `${taskCompletionPercent}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 mt-1">{taskCompletionPercent}% Complete</p>
        </div>

        {/* Budget */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-gray-900">Budget</h3>
            <DollarSign className="w-5 h-5 text-amber-600" />
          </div>
          <p className="text-3xl font-bold text-amber-600">
            ${stats?.totalSpent?.toLocaleString() || 0}
          </p>
          <p className="text-sm text-gray-600 mt-1">
            of ${stats?.budgetGoal?.toLocaleString() || 0} budget
          </p>
          <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
            <div
              className={`h-2 rounded-full transition-all ${
                isOverBudget ? 'bg-red-600' : 'bg-amber-600'
              }`}
              style={{ width: `${Math.min(Number(budgetPercent), 100)}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 mt-1">{budgetPercent}% Spent</p>
        </div>

        {/* Timeline */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-gray-900">Days Left</h3>
            <Calendar className="w-5 h-5 text-purple-600" />
          </div>
          <p className={`text-3xl font-bold ${isTimePressure ? 'text-red-600' : 'text-purple-600'}`}>
            {stats?.daysToWedding || '—'}
          </p>
          <p className="text-sm text-gray-600 mt-1">
            {stats && stats.daysToWedding > 0
              ? `${stats.daysToWedding} days until wedding`
              : 'Set your wedding date'}
          </p>
        </div>

        {/* Sentiment Trend */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-gray-900">Mood</h3>
            <TrendingUp className="w-5 h-5 text-indigo-600" />
          </div>
          <p className="text-lg font-semibold text-indigo-600 capitalize">
            {stats?.sentimentTrend || '—'}
          </p>
          <p className="text-sm text-gray-600 mt-1">Overall sentiment trend</p>
        </div>

        {/* Pending Tasks */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-gray-900">Pending</h3>
            <AlertCircle className="w-5 h-5 text-red-600" />
          </div>
          <p className="text-3xl font-bold text-red-600">{stats?.pendingTasks || 0}</p>
          <p className="text-sm text-gray-600 mt-1">Tasks to complete</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6">
        <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <button className="bg-white border border-gray-200 rounded-lg p-3 text-sm font-medium text-gray-700 hover:border-blue-300 hover:bg-blue-50 transition-colors">
            New Entry
          </button>
          <button className="bg-white border border-gray-200 rounded-lg p-3 text-sm font-medium text-gray-700 hover:border-blue-300 hover:bg-blue-50 transition-colors">
            View Tasks
          </button>
          <button className="bg-white border border-gray-200 rounded-lg p-3 text-sm font-medium text-gray-700 hover:border-blue-300 hover:bg-blue-50 transition-colors">
            Search Entries
          </button>
          <button className="bg-white border border-gray-200 rounded-lg p-3 text-sm font-medium text-gray-700 hover:border-blue-300 hover:bg-blue-50 transition-colors">
            Get Insights
          </button>
        </div>
      </div>
    </div>
  );
}
