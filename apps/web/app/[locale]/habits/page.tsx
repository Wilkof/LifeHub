'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import { cn } from '@/app/lib/utils';
import { Plus, Check, Flame, MoreHorizontal } from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

const mockHabits = [
  { id: 1, name: 'Медитація', icon: '🧘', color: '#8b5cf6', streak: 12, completed: true },
  { id: 2, name: 'Читання', icon: '📚', color: '#3b82f6', streak: 7, completed: false },
  { id: 3, name: 'Спорт', icon: '💪', color: '#10b981', streak: 5, completed: true },
  { id: 4, name: 'Вода (8 склянок)', icon: '💧', color: '#06b6d4', streak: 14, completed: false },
  { id: 5, name: 'Без соцмереж до 12:00', icon: '📵', color: '#f59e0b', streak: 3, completed: true },
  { id: 6, name: 'Щоденник', icon: '📝', color: '#ec4899', streak: 21, completed: false },
];

// Generate week calendar
const weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'];
const today = new Date();
const weekData = Array.from({ length: 7 }, (_, i) => {
  const date = new Date(today);
  date.setDate(today.getDate() - today.getDay() + i + 1);
  return {
    day: weekDays[i],
    date: date.getDate(),
    isToday: date.toDateString() === today.toDateString(),
  };
});

export default function HabitsPage({ params: { locale } }: PageProps) {
  const t = useTranslations('habits');
  const [habits, setHabits] = useState(mockHabits);

  const toggleHabit = (id: number) => {
    setHabits((prev) =>
      prev.map((h) => (h.id === id ? { ...h, completed: !h.completed } : h))
    );
  };

  const completedCount = habits.filter((h) => h.completed).length;

  return (
    <div className="max-w-4xl">
      <Header locale={locale} title={t('title')} />

      {/* Week calendar */}
      <Card className="mb-6">
        <div className="flex justify-between">
          {weekData.map((day, i) => (
            <div
              key={i}
              className={cn(
                'flex flex-col items-center p-3 rounded-2xl',
                day.isToday && 'bg-lime-500'
              )}
            >
              <span className={cn('text-sm', day.isToday ? 'text-dark-900' : 'text-dark-400')}>
                {day.day}
              </span>
              <span className={cn('text-2xl font-bold', day.isToday && 'text-dark-900')}>
                {day.date}
              </span>
            </div>
          ))}
        </div>
      </Card>

      {/* Summary */}
      <div className="flex items-center justify-between mb-6">
        <div className="text-lg">
          <span className="font-bold">{completedCount}</span>
          <span className="text-dark-500"> / {habits.length} {t('completed')}</span>
        </div>
        <button className="btn btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" />
          {t('newHabit')}
        </button>
      </div>

      {/* Habits list */}
      <div className="space-y-3">
        {habits.map((habit) => (
          <Card
            key={habit.id}
            className="flex items-center gap-4 p-4"
          >
            {/* Checkbox */}
            <button
              onClick={() => toggleHabit(habit.id)}
              className={cn(
                'w-12 h-12 rounded-xl flex items-center justify-center text-2xl transition-all',
                habit.completed
                  ? 'bg-lime-500'
                  : 'bg-sage-100 hover:bg-sage-200'
              )}
              style={{
                backgroundColor: habit.completed ? habit.color : undefined,
              }}
            >
              {habit.completed ? (
                <Check className="w-6 h-6 text-white" />
              ) : (
                habit.icon
              )}
            </button>

            {/* Habit info */}
            <div className="flex-1">
              <div className="font-medium">{habit.name}</div>
              <div className="flex items-center gap-2 text-sm text-dark-500">
                <Flame className="w-4 h-4 text-orange-500" />
                <span>{habit.streak} {t('days')} {t('streak')}</span>
              </div>
            </div>

            {/* Week progress */}
            <div className="flex gap-1">
              {[1, 1, 1, 0, 1, 0, 0].map((done, i) => (
                <div
                  key={i}
                  className={cn(
                    'w-6 h-6 rounded-lg',
                    done ? 'bg-lime-400' : 'bg-dark-200'
                  )}
                  style={{
                    backgroundColor: done ? habit.color : undefined,
                  }}
                />
              ))}
            </div>

            {/* More menu */}
            <button className="p-2 hover:bg-dark-100 rounded-lg">
              <MoreHorizontal className="w-4 h-4 text-dark-400" />
            </button>
          </Card>
        ))}
      </div>
    </div>
  );
}
