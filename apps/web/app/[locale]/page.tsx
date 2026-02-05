'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import RightSidebar from '@/app/components/layout/RightSidebar';
import Card, { StatCard } from '@/app/components/ui/Card';
import { api } from '@/app/lib/api';
import { cn } from '@/app/lib/utils';
import { Calendar, CheckCircle2, Flame, Droplets, Bot } from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

export default function DashboardPage({ params: { locale } }: PageProps) {
  const t = useTranslations('dashboard');
  const [data, setData] = useState<any>(null);
  const [briefing, setBriefing] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getDashboardToday();
      setData(res);
    } catch (err: any) {
      setError(err?.message || 'Помилка завантаження');
    } finally {
      setLoading(false);
    }
  };

  const loadBriefing = async () => {
    try {
      const res = await api.getDailyBriefing();
      setBriefing(res?.briefing || '');
    } catch (err) {
      setBriefing('Не вдалося згенерувати брифінг.');
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="flex gap-6">
      {/* Main Content */}
      <div className="flex-1">
        <Header locale={locale} title="LifeHub Dashboard" />

        {error && (
          <Card className="mb-6 border border-red-200 bg-red-50 text-red-700">
            {error}
          </Card>
        )}

        {/* Stats Row */}
        <div className="grid grid-cols-3 gap-6 mb-8">
          <StatCard
            title="Задачі"
            value={data?.stats?.completed_today ?? 0}
            subtitle={`/ ${data?.stats?.total_pending ?? 0}`}
            percentage={undefined}
            icon={<CheckCircle2 className="w-4 h-4" />}
            bars={[0.2, 0.4, 0.6, 0.8, 0.7, 0.5]}
          />

          <StatCard
            title="Звички"
            value={data?.stats?.habits_completed ?? 0}
            subtitle={`/ ${data?.stats?.habits_total ?? 0}`}
            variant="lime"
            icon={<Flame className="w-4 h-4" />}
            bars={[0.3, 0.5, 0.7, 0.6, 0.8, 0.4]}
          />

          <StatCard
            title="Вода"
            value={data?.health?.water_glasses ?? 0}
            subtitle="склянок"
            icon={<Droplets className="w-4 h-4" />}
            bars={[0.1, 0.2, 0.3, 0.4, 0.6, 0.8]}
          />
        </div>

        {/* Main Sections */}
        <div className="grid grid-cols-2 gap-6 mb-8">
          <Card>
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle2 className="w-5 h-5 text-dark-600" />
              <h2 className="text-lg font-semibold">{t('mit')}</h2>
            </div>
            {data?.mit_tasks?.length ? (
              <ul className="space-y-2">
                {data.mit_tasks.map((task: any) => (
                  <li key={task.id} className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-lime-500" />
                    <span>{task.title}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-sm text-dark-500">{t('mitEmpty')}</div>
            )}
          </Card>

          <Card>
            <div className="flex items-center gap-2 mb-4">
              <Calendar className="w-5 h-5 text-dark-600" />
              <h2 className="text-lg font-semibold">{t('todayTasks')}</h2>
            </div>
            {data?.today_tasks?.length ? (
              <ul className="space-y-2">
                {data.today_tasks.map((task: any) => (
                  <li key={task.id} className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-dark-400" />
                    <span>{task.title}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-sm text-dark-500">{t('noTasks')}</div>
            )}
          </Card>
        </div>

        <Card>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Bot className="w-5 h-5 text-dark-600" />
              <h2 className="text-lg font-semibold">Daily Briefing</h2>
            </div>
            <button className="btn btn-secondary" onClick={loadBriefing}>
              Згенерувати
            </button>
          </div>
          <div className={cn('text-sm text-dark-700', !briefing && 'text-dark-400')}>
            {briefing || 'Натисніть “Згенерувати”, щоб отримати AI-брифінг.'}
          </div>
        </Card>
      </div>

      {/* Right Sidebar */}
      <RightSidebar />
    </div>
  );
}
