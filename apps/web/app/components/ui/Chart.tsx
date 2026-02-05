'use client';

import { cn } from '@/app/lib/utils';

interface ChartBarProps {
  data: {
    label: string;
    value1: number; // Operations
    value2: number; // Data transfer
    percentage?: number;
  }[];
  maxValue?: number;
}

export default function ChartBar({ data, maxValue = 1 }: ChartBarProps) {
  return (
    <div className="flex items-end justify-between gap-4 h-64">
      {data.map((item, i) => (
        <div key={i} className="flex-1 flex flex-col items-center gap-2">
          {/* Bars container */}
          <div className="flex-1 w-full flex items-end gap-1">
            {/* Dark bar (Operations) */}
            <div
              className="flex-1 bg-dark-800 rounded-t-full relative transition-all duration-500"
              style={{ height: `${(item.value1 / maxValue) * 100}%` }}
            >
              {/* Dot at top */}
              <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-3 h-3 bg-lime-400 rounded-full" />
              {item.percentage && (
                <div className="absolute -top-8 left-1/2 -translate-x-1/2 text-xs bg-dark-800 text-white px-2 py-0.5 rounded-full whitespace-nowrap">
                  {item.percentage}%
                </div>
              )}
            </div>
            
            {/* Lime bar (Data transfer) */}
            <div
              className="flex-1 bg-lime-400 rounded-t-full relative transition-all duration-500"
              style={{ height: `${(item.value2 / maxValue) * 100}%` }}
            >
              <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-3 h-3 bg-lime-600 rounded-full" />
            </div>
          </div>
          
          {/* Label */}
          <span className="text-xs text-dark-500">{item.label}</span>
        </div>
      ))}
    </div>
  );
}

// Y-axis labels
export function ChartYAxis({ labels }: { labels: string[] }) {
  return (
    <div className="flex flex-col justify-between h-64 text-xs text-dark-400 pr-4">
      {labels.map((label, i) => (
        <span key={i}>{label}</span>
      ))}
    </div>
  );
}

// Legend
interface LegendItem {
  color: string;
  label: string;
}

export function ChartLegend({ items }: { items: LegendItem[] }) {
  return (
    <div className="flex items-center gap-4">
      {items.map((item, i) => (
        <div key={i} className="flex items-center gap-2">
          <div
            className="w-3 h-3 rounded-full"
            style={{ backgroundColor: item.color }}
          />
          <span className="text-sm text-dark-600">{item.label}</span>
        </div>
      ))}
    </div>
  );
}
