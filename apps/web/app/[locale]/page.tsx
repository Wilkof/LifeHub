'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import RightSidebar from '@/app/components/layout/RightSidebar';
import Card, { StatCard, PromoCard } from '@/app/components/ui/Card';
import Tabs from '@/app/components/ui/Tabs';
import ChartBar, { ChartYAxis, ChartLegend } from '@/app/components/ui/Chart';
import { Settings as SettingsIcon, ArrowDownUp, TrendingUp } from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

export default function DashboardPage({ params: { locale } }: PageProps) {
  const t = useTranslations('dashboard');
  const tNav = useTranslations('nav');
  const [activeTab, setActiveTab] = useState('organization');

  const tabs = [
    { key: 'organization', label: 'Organization' },
    { key: 'teams', label: 'Teams' },
    { key: 'users', label: 'Users' },
    { key: 'subscription', label: 'Subscription' },
    { key: 'payment', label: 'Payment' },
    { key: 'apps', label: 'Installed Apps' },
    { key: 'variables', label: 'Variables' },
    { key: 'properties', label: 'Scenario Properties' },
  ];

  // Mock chart data
  const chartData = [
    { label: '27 Jun', value1: 0.3, value2: 0.2 },
    { label: '28 Jun', value1: 0.55, value2: 0.35 },
    { label: '29 Jun', value1: 0.5, value2: 0.25 },
    { label: '30 Jun', value1: 0.45, value2: 0.3, percentage: 32 },
    { label: '1 Jul', value1: 0.85, value2: 0.7, percentage: 87 },
    { label: '2 Jul', value1: 0.65, value2: 0.45 },
    { label: '3 Jul', value1: 0.55, value2: 0.4 },
    { label: '4 Jul', value1: 0.5, value2: 0.35 },
  ];

  return (
    <div className="flex gap-6">
      {/* Main Content */}
      <div className="flex-1">
        <Header locale={locale} title="Managing ⚙ Your Team and ✨ Workflows" />

        {/* Tabs */}
        <Tabs
          tabs={tabs}
          activeTab={activeTab}
          onChange={setActiveTab}
          className="mb-8"
        />

        {/* Stats Row */}
        <div className="grid grid-cols-3 gap-6 mb-8">
          {/* Operations Card */}
          <StatCard
            title="Operations"
            value="780"
            subtitle="/ 1 000"
            percentage={82}
            icon={<SettingsIcon className="w-4 h-4" />}
            bars={[0.7, 0.8, 0.9, 0.85, 0.75, 0.8]}
          />

          {/* Data Transfer Card */}
          <StatCard
            title="Data Transfer"
            value="163"
            subtitle="/ 512.0 MB"
            percentage={68}
            variant="lime"
            icon={<ArrowDownUp className="w-4 h-4" />}
            bars={[0.5, 0.6, 0.7, 0.65, 0.55, 0.6]}
          />

          {/* Promo Card */}
          <PromoCard
            title="Take Your ↗ Automation to the Next Level"
            buttonText="Upgrade"
          />
        </div>

        {/* Statistics Section */}
        <Card className="p-8">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-4">
              <TrendingUp className="w-5 h-5 text-dark-600" />
              <h2 className="text-xl font-bold">Statistics</h2>
              <ChartLegend
                items={[
                  { color: '#262626', label: 'Operations' },
                  { color: '#c8e972', label: 'Data transfer' },
                ]}
              />
            </div>
            <select className="input w-32">
              <option>2025</option>
              <option>2024</option>
            </select>
          </div>

          <div className="flex">
            <ChartYAxis labels={['1.0', '0.9', '0.8', '0.7', '0.6', '0.5', '0.4', '0.3', '0.2', '0.1']} />
            <div className="flex-1">
              <ChartBar data={chartData} maxValue={1} />
            </div>
          </div>
        </Card>
      </div>

      {/* Right Sidebar */}
      <RightSidebar />
    </div>
  );
}
