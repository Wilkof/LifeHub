'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import { api } from '@/app/lib/api';
import { Target } from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

export default function GoalsPage({ params: { locale } }: PageProps) {
  const t = useTranslations('goals');
  const [goals, setGoals] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getActiveGoals()
      .then(setGoals)
      .catch((err) => setError(err?.message || 'Не вдалося завантажити цілі'));
  }, []);

  return (
    <div className="max-w-4xl">
      <Header locale={locale} title={t('title')} />

      {error && (
        <Card className="mb-4 border border-red-200 bg-red-50 text-red-700">
          {error}
        </Card>
      )}

      <div className="space-y-3">
        {goals.length ? (
          goals.map((goal) => (
            <Card key={goal.id}>
              <div className="flex items-center gap-3 mb-2">
                <Target className="w-5 h-5 text-dark-600" />
                <div className="font-medium">{goal.title}</div>
              </div>
              <div className="text-sm text-dark-500 mb-2">{goal.description || '—'}</div>
              <div className="w-full bg-sage-100 rounded-full h-2">
                <div
                  className="bg-lime-500 h-2 rounded-full"
                  style={{ width: `${goal.progress ?? 0}%` }}
                />
              </div>
              <div className="text-xs text-dark-500 mt-2">{goal.progress ?? 0}%</div>
            </Card>
          ))
        ) : (
          <Card className="text-center py-8">Немає активних цілей</Card>
        )}
      </div>
    </div>
  );
}
