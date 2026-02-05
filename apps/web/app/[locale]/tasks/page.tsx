'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import Tabs from '@/app/components/ui/Tabs';
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

// Mock tasks data
const mockTasks = [
  {
    id: 1,
    title: 'Завершити дизайн дашборду',
    status: 'in_progress',
    priority: 'high',
    is_mit: true,
    due_date: '2026-02-06',
    tags: ['design', 'frontend'],
  },
  {
    id: 2,
    title: 'Написати документацію API',
    status: 'todo',
    priority: 'medium',
    is_mit: true,
    due_date: '2026-02-07',
    tags: ['docs', 'backend'],
  },
  {
    id: 3,
    title: 'Налаштувати CI/CD',
    status: 'todo',
    priority: 'high',
    is_mit: false,
    due_date: '2026-02-08',
    tags: ['devops'],
  },
  {
    id: 4,
    title: 'Тестування Telegram бота',
    status: 'done',
    priority: 'medium',
    is_mit: false,
    due_date: '2026-02-05',
    tags: ['telegram', 'testing'],
  },
  {
    id: 5,
    title: 'Оптимізувати запити до БД',
    status: 'backlog',
    priority: 'low',
    is_mit: false,
    due_date: null,
    tags: ['backend', 'optimization'],
  },
];

export default function TasksPage({ params: { locale } }: PageProps) {
  const t = useTranslations('tasks');
  const [activeTab, setActiveTab] = useState('all');
  const [tasks, setTasks] = useState(mockTasks);

  const tabs = [
    { key: 'all', label: 'Всі' },
    { key: 'today', label: 'Сьогодні' },
    { key: 'mit', label: '🎯 MIT' },
    { key: 'in_progress', label: 'В процесі' },
    { key: 'done', label: 'Виконані' },
  ];

  const filteredTasks = tasks.filter((task) => {
    if (activeTab === 'all') return task.status !== 'done';
    if (activeTab === 'mit') return task.is_mit;
    if (activeTab === 'today') return task.due_date === '2026-02-05';
    return task.status === activeTab;
  });

  const toggleComplete = (taskId: number) => {
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId
          ? { ...task, status: task.status === 'done' ? 'todo' : 'done' }
          : task
      )
    );
  };

  return (
    <div className="max-w-5xl">
      <Header locale={locale} title={t('title')} />

      {/* Actions bar */}
      <div className="flex items-center justify-between mb-6">
        <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />
        <button className="btn btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" />
          {t('newTask')}
        </button>
      </div>

      {/* Tasks list */}
      <div className="space-y-3">
        {filteredTasks.map((task) => (
          <Card key={task.id} className="flex items-center gap-4 p-4">
            {/* Checkbox */}
            <button
              onClick={() => toggleComplete(task.id)}
              className="flex-shrink-0"
            >
              {task.status === 'done' ? (
                <CheckCircle2 className="w-6 h-6 text-green-500" />
              ) : (
                <Circle className="w-6 h-6 text-dark-300 hover:text-dark-500" />
              )}
            </button>

            {/* MIT star */}
            <button className="flex-shrink-0">
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
                priorityColors[task.priority as keyof typeof priorityColors]
              )}
            >
              {t(`priorities.${task.priority}`)}
            </span>

            {/* Status badge */}
            <span
              className={cn(
                'pill text-xs',
                statusColors[task.status as keyof typeof statusColors]
              )}
            >
              {t(`statuses.${task.status}`)}
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
