'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import { api } from '@/app/lib/api';
import { Calendar as CalendarIcon, MapPin } from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

export default function CalendarPage({ params: { locale } }: PageProps) {
  const t = useTranslations('calendar');
  const [events, setEvents] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getTodayEvents()
      .then(setEvents)
      .catch((err) => setError(err?.message || 'Не вдалося завантажити події'));
  }, []);

  return (
    <div className="max-w-4xl">
      <Header locale={locale} title={t('title')} />

      {error && (
        <Card className="mb-4 border border-red-200 bg-red-50 text-red-700">
          {error}
        </Card>
      )}

      <Card>
        <div className="flex items-center gap-2 mb-4">
          <CalendarIcon className="w-5 h-5 text-dark-600" />
          <h2 className="text-lg font-semibold">{t('weekView')}</h2>
        </div>

        {events.length ? (
          <div className="space-y-3">
            {events.map((event) => (
              <div key={event.id} className="flex items-start gap-3 p-3 rounded-2xl bg-sage-100">
                <div
                  className="w-3 h-3 rounded-full mt-2"
                  style={{ backgroundColor: event.color || '#3b82f6' }}
                />
                <div className="flex-1">
                  <div className="font-medium">{event.title}</div>
                  <div className="text-sm text-dark-500">
                    {event.start_time?.slice(11, 16)} {event.end_time ? `– ${event.end_time.slice(11, 16)}` : ''}
                  </div>
                  {event.location && (
                    <div className="text-xs text-dark-400 flex items-center gap-1">
                      <MapPin className="w-3 h-3" />
                      {event.location}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-sm text-dark-500">{t('noEvents')}</div>
        )}
      </Card>
    </div>
  );
}
