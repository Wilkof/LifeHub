'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import { api } from '@/app/lib/api';
import { formatCurrency } from '@/app/lib/utils';
import { Wallet, TrendingUp, TrendingDown } from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

export default function FinancesPage({ params: { locale } }: PageProps) {
  const t = useTranslations('finances');
  const [summary, setSummary] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getTransactionsSummary()
      .then(setSummary)
      .catch((err) => setError(err?.message || 'Не вдалося завантажити фінанси'));
  }, []);

  return (
    <div className="max-w-4xl">
      <Header locale={locale} title={t('title')} />

      {error && (
        <Card className="mb-4 border border-red-200 bg-red-50 text-red-700">
          {error}
        </Card>
      )}

      <div className="grid grid-cols-3 gap-6">
        <Card>
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-5 h-5 text-green-600" />
            <div className="text-sm text-dark-500">{t('income')}</div>
          </div>
          <div className="text-2xl font-bold">
            {formatCurrency(summary?.income || 0)}
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-2 mb-2">
            <TrendingDown className="w-5 h-5 text-red-600" />
            <div className="text-sm text-dark-500">{t('expenses')}</div>
          </div>
          <div className="text-2xl font-bold">
            {formatCurrency(summary?.expenses || 0)}
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-2 mb-2">
            <Wallet className="w-5 h-5 text-dark-600" />
            <div className="text-sm text-dark-500">{t('balance')}</div>
          </div>
          <div className="text-2xl font-bold">
            {formatCurrency(summary?.balance || 0)}
          </div>
        </Card>
      </div>
    </div>
  );
}
