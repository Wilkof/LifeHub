'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import { api } from '@/app/lib/api';
import { cn } from '@/app/lib/utils';
import { Plus, Check, Flame, MoreHorizontal } from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

interface HabitItem {
  id: number;
  name: string;
  icon: string;
  color: string;
  completed: boolean;
  current_streak?: number;
  preferred_time?: string | null;
}

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
  const [habits, setHabits] = useState<HabitItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newHabitName, setNewHabitName] = useState('');

  const loadHabits = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getTodayHabits();
      setHabits(data);
    } catch (err: any) {
      setError(err?.message || 'Помилка завантаження звичок');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHabits();
  }, []);

  const toggleHabit = async (habit: HabitItem) => {
    try {
      if (habit.completed) {
        await api.uncompleteHabit(habit.id);
      } else {
        await api.completeHabit(habit.id);
      }
      await loadHabits();
    } catch (err: any) {
      setError(err?.message || 'Не вдалося оновити звичку');
    }
  };

  const addHabit = async () => {
    if (!newHabitName.trim()) return;
    try {
      await api.createHabit({ name: newHabitName.trim() });
      setNewHabitName('');
      await loadHabits();
    } catch (err: any) {
      setError(err?.message || 'Не вдалося створити звичку');
    }
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
        <button className="btn btn-primary flex items-center gap-2" onClick={addHabit}>
          <Plus className="w-4 h-4" />
          {t('newHabit')}
        </button>
      </div>

      <Card className="mb-4">
        <div className="flex gap-3">
          <input
            className="input flex-1"
            placeholder={t('newHabit')}
            value={newHabitName}
            onChange={(e) => setNewHabitName(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addHabit()}
          />
          <button className="btn btn-primary" onClick={addHabit}>
            {t('add')}
          </button>
        </div>
      </Card>

      {error && (
        <Card className="mb-4 border border-red-200 bg-red-50 text-red-700">
          {error}
        </Card>
      )}

      {/* Habits list */}
      <div className="space-y-3">
        {loading && <Card className="text-center py-8">Завантаження...</Card>}
        {habits.map((habit) => (
          <Card
            key={habit.id}
            className="flex items-center gap-4 p-4"
          >
            {/* Checkbox */}
            <button
              onClick={() => toggleHabit(habit)}
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
                <span>{habit.current_streak ?? 0} {t('days')} {t('streak')}</span>
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
