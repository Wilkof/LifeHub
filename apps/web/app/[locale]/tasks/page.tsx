'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import Tabs from '@/app/components/ui/Tabs';
import { api } from '@/app/lib/api';
import { cn, priorityColors, statusColors } from '@/app/lib/utils';
import {
  Plus,
  CheckCircle2,
  Circle,
  Star,
  Calendar,
  Tag,
  MoreHorizontal,
} from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

interface TaskItem {
  id: number;
  title: string;
  status: string;
  priority: string;
  is_mit: boolean;
  due_date?: string | null;
  tags?: string[];
}

export default function TasksPage({ params: { locale } }: PageProps) {
  const t = useTranslations('tasks');
  const [activeTab, setActiveTab] = useState('all');
  const [tasks, setTasks] = useState<TaskItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newTitle, setNewTitle] = useState('');

  const tabs = [
    { key: 'all', label: 'Всі' },
    { key: 'today', label: 'Сьогодні' },
    { key: 'mit', label: '🎯 MIT' },
    { key: 'in_progress', label: 'В процесі' },
    { key: 'done', label: 'Виконані' },
  ];

  const loadTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getTasks();
      setTasks(data);
    } catch (err: any) {
      setError(err?.message || 'Помилка завантаження задач');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const filteredTasks = tasks.filter((task) => {
    if (activeTab === 'all') return task.status !== 'done';
    if (activeTab === 'mit') return task.is_mit;
    if (activeTab === 'today') return task.due_date;
    return task.status === activeTab;
  });

  const toggleComplete = async (task: TaskItem) => {
    try {
      if (task.status === 'done') {
        await api.updateTask(task.id, { status: 'todo' });
      } else {
        await api.completeTask(task.id);
      }
      await loadTasks();
    } catch (err: any) {
      setError(err?.message || 'Не вдалося оновити задачу');
    }
  };

  const toggleMit = async (taskId: number) => {
    try {
      await api.toggleMit(taskId);
      await loadTasks();
    } catch (err: any) {
      setError(err?.message || 'Не вдалося оновити MIT');
    }
  };

  const addTask = async () => {
    if (!newTitle.trim()) return;
    try {
      await api.createTask({ title: newTitle.trim() });
      setNewTitle('');
      await loadTasks();
    } catch (err: any) {
      setError(err?.message || 'Не вдалося створити задачу');
    }
  };

  return (
    <div className="max-w-5xl">
      <Header locale={locale} title={t('title')} />

      {/* Actions bar */}
      <div className="flex items-center justify-between mb-6">
        <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />
        <button className="btn btn-primary flex items-center gap-2" onClick={addTask}>
          <Plus className="w-4 h-4" />
          {t('newTask')}
        </button>
      </div>

      <Card className="mb-4">
        <div className="flex gap-3">
          <input
            className="input flex-1"
            placeholder={t('taskTitle')}
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addTask()}
          />
          <button className="btn btn-primary" onClick={addTask}>
            {t('add')}
          </button>
        </div>
      </Card>

      {error && (
        <Card className="mb-4 border border-red-200 bg-red-50 text-red-700">
          {error}
        </Card>
      )}

      {/* Tasks list */}
      <div className="space-y-3">
        {loading && <Card className="text-center py-8">Завантаження...</Card>}
        {filteredTasks.map((task) => (
          <Card key={task.id} className="flex items-center gap-4 p-4">
            {/* Checkbox */}
            <button
              onClick={() => toggleComplete(task)}
              className="flex-shrink-0"
            >
              {task.status === 'done' ? (
                <CheckCircle2 className="w-6 h-6 text-green-500" />
              ) : (
                <Circle className="w-6 h-6 text-dark-300 hover:text-dark-500" />
              )}
            </button>

            {/* MIT star */}
            <button className="flex-shrink-0" onClick={() => toggleMit(task.id)}>
              <Star
                className={cn(
                  'w-5 h-5',
                  task.is_mit
                    ? 'text-yellow-500 fill-yellow-500'
                    : 'text-dark-300 hover:text-yellow-500'
                )}
              />
            </button>

            {/* Task content */}
            <div className="flex-1 min-w-0">
              <div
                className={cn(
                  'font-medium',
                  task.status === 'done' && 'line-through text-dark-400'
                )}
              >
                {task.title}
              </div>
              <div className="flex items-center gap-3 mt-1">
                {task.due_date && (
                  <span className="flex items-center gap-1 text-xs text-dark-500">
                    <Calendar className="w-3 h-3" />
                    {task.due_date}
                  </span>
                )}
                {task.tags.map((tag) => (
                  <span
                    key={tag}
                    className="flex items-center gap-1 text-xs text-dark-400"
                  >
                    <Tag className="w-3 h-3" />
                    {tag}
                  </span>
                ))}
              </div>
            </div>

            {/* Priority badge */}
            <span
              className={cn(
                'pill text-xs',
                priorityColors[task.priority as keyof typeof priorityColors] || 'bg-gray-100 text-gray-800'
              )}
            >
              {t(`priorities.${task.priority}`) || task.priority}
            </span>

            {/* Status badge */}
            <span
              className={cn(
                'pill text-xs',
                statusColors[task.status as keyof typeof statusColors] || 'bg-gray-100 text-gray-800'
              )}
            >
              {t(`statuses.${task.status}`) || task.status}
            </span>

            {/* More menu */}
            <button className="p-2 hover:bg-dark-100 rounded-lg">
              <MoreHorizontal className="w-4 h-4 text-dark-400" />
            </button>
          </Card>
        ))}

        {filteredTasks.length === 0 && (
          <Card className="text-center py-12">
            <p className="text-dark-500">{t('noTasks')}</p>
          </Card>
        )}
      </div>
    </div>
  );
}
