'use client'

import { useState } from 'react'
import { useStore } from '@/lib/store'
import { apiClient } from '@/lib/api'
import { Circle, Trash2, Plus } from 'lucide-react'

export default function TaskPanel() {
  const { tasks, removeTask, setTasks } = useStore()
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    action: '',
    priority: 'medium',
  })

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.action.trim()) {
      return
    }

    try {
      const task = await apiClient.createTask(
        formData.action,
        undefined,
        undefined,
        formData.priority
      )
      setTasks([...tasks, task])
      setFormData({ action: '', priority: 'medium' })
      setShowForm(false)
    } catch (error: any) {
      console.error('Failed to create task:', error)
    }
  }

  const handleCompleteTask = async (taskId: string) => {
    try {
      await apiClient.completeTask(taskId)
      removeTask(taskId)
    } catch (error: any) {
      console.error('Failed to complete task:', error)
    }
  }

  const pendingTasks = tasks.filter((t) => t.status === 'pending')

  return (
    <div className="space-y-6">
      {/* Tasks Card */}
      <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold text-gray-900">Tasks</h3>
          <button
            onClick={() => setShowForm(!showForm)}
            className="text-primary hover:text-primary/80 transition-colors"
          >
            <Plus className="w-5 h-5" />
          </button>
        </div>

        {showForm && (
          <form onSubmit={handleCreateTask} className="mb-4 pb-4 border-b border-gray-100 space-y-3">
            <input
              type="text"
              value={formData.action}
              onChange={(e) => setFormData({ ...formData, action: e.target.value })}
              placeholder="Add a new task..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
            />
            <div className="flex gap-2">
              <select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
              <button
                type="submit"
                className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors text-sm font-medium"
              >
                Add
              </button>
            </div>
          </form>
        )}

        {pendingTasks.length === 0 ? (
          <p className="text-gray-500 text-sm text-center py-4">No pending tasks</p>
        ) : (
          <div className="space-y-2">
            {pendingTasks.map((task) => (
              <div
                key={task.id}
                className="flex items-start gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors group"
              >
                <button
                  onClick={() => handleCompleteTask(task.id)}
                  className="flex-shrink-0 text-gray-400 hover:text-green-600 transition-colors mt-0.5"
                >
                  <Circle className="w-5 h-5" />
                </button>

                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 break-words">
                    {task.action}
                  </p>
                  <div className="flex items-center gap-2 mt-1">
                    <span
                      className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                        task.priority === 'critical'
                          ? 'bg-red-100 text-red-700'
                          : task.priority === 'high'
                            ? 'bg-orange-100 text-orange-700'
                            : task.priority === 'medium'
                              ? 'bg-blue-100 text-blue-700'
                              : 'bg-gray-100 text-gray-700'
                      }`}
                    >
                      {task.priority}
                    </span>
                    {task.deadline && (
                      <span className="text-xs text-gray-600">
                        Due {new Date(task.deadline).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>

                <button
                  onClick={() => removeTask(task.id)}
                  className="flex-shrink-0 text-gray-300 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Stats Card */}
      <div className="bg-gradient-to-br from-primary/5 to-secondary/5 rounded-xl shadow-sm p-6 border border-primary/10">
        <h4 className="text-sm font-semibold text-gray-900 mb-4">Progress</h4>
        <div className="space-y-3">
          <div>
            <p className="text-2xl font-bold text-primary">{pendingTasks.length}</p>
            <p className="text-sm text-gray-600">Pending tasks</p>
          </div>
        </div>
      </div>
    </div>
  )
}
