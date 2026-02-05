'use client';

import { cn } from '@/app/lib/utils';

interface Tab {
  key: string;
  label: string;
}

interface TabsProps {
  tabs: Tab[];
  activeTab: string;
  onChange: (key: string) => void;
  className?: string;
}

export default function Tabs({ tabs, activeTab, onChange, className }: TabsProps) {
  return (
    <div className={cn('flex items-center gap-2 p-1 bg-sage-200/50 rounded-full', className)}>
      {tabs.map((tab) => (
        <button
          key={tab.key}
          onClick={() => onChange(tab.key)}
          className={cn(
            'tab',
            activeTab === tab.key ? 'tab-active' : 'tab-inactive'
          )}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
