'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import { api } from '@/app/lib/api';
import { BarChart3 } from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

export default function AnalyticsPage({ params: { locale } }: PageProps) {
  const t = useTranslations('nav');
  const [weekly, setWeekly] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getWeeklyOverview()
      .then(setWeekly)
      .catch((err) => setError(err?.message || 'Не вдалося завантажити аналітику'));
  }, []);

  return (
    <div className="max-w-4xl">
      <Header locale={locale} title={t('analytics')} />

      {error && (
        <Card className="mb-4 border border-red-200 bg-red-50 text-red-700">
          {error}
        </Card>
      )}

      <Card>
        <div className="flex items-center gap-2 mb-4">
          <BarChart3 className="w-5 h-5 text-dark-600" />
          <h2 className="text-lg font-semibold">Weekly overview</h2>
        </div>
        <div className="grid grid-cols-3 gap-4">
          <div className="p-4 rounded-2xl bg-sage-100">
            <div className="text-sm text-dark-500">Задач виконано</div>
            <div className="text-2xl font-bold">{weekly?.tasks_completed ?? 0}</div>
          </div>
          <div className="p-4 rounded-2xl bg-sage-100">
            <div className="text-sm text-dark-500">Звички</div>
            <div className="text-2xl font-bold">{weekly?.habits?.completion_rate ?? 0}%</div>
          </div>
          <div className="p-4 rounded-2xl bg-sage-100">
            <div className="text-sm text-dark-500">Витрати</div>
            <div className="text-2xl font-bold">{weekly?.expenses ?? 0}</div>
          </div>
        </div>
      </Card>
    </div>
  );
}
