'use client';

import { ReactNode } from 'react';
import { cn } from '@/app/lib/utils';

interface CardProps {
  children: ReactNode;
  className?: string;
  variant?: 'default' | 'dark' | 'lime';
  padding?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
}

export default function Card({
  children,
  className,
  variant = 'default',
  padding = 'md',
  onClick,
}: CardProps) {
  const variants = {
    default: 'bg-white',
    dark: 'bg-dark-800 text-white',
    lime: 'bg-lime-500 text-dark-900',
  };

  const paddings = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  return (
    <div
      className={cn(
        'rounded-3xl shadow-card transition-all duration-200',
        variants[variant],
        paddings[padding],
        onClick && 'cursor-pointer hover:shadow-card-hover',
        className
      )}
      onClick={onClick}
    >
      {children}
    </div>
  );
}

// Stat Card component (like Operations/Data Transfer in screenshot)
interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  percentage?: number;
  icon?: ReactNode;
  variant?: 'default' | 'lime';
  bars?: number[]; // Array of values 0-1 for bar chart
}

export function StatCard({
  title,
  value,
  subtitle,
  percentage,
  icon,
  variant = 'default',
  bars,
}: StatCardProps) {
  return (
    <Card
      variant={variant}
      className={cn(
        'relative',
        variant === 'lime' && 'bg-lime-500'
      )}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-2">
          {icon && <div className="text-dark-500">{icon}</div>}
          <span className="text-sm text-dark-500">{title}</span>
        </div>
        {percentage !== undefined && (
          <div className="flex items-center gap-1 text-sm">
            <span className={cn(
              percentage >= 0 ? 'text-green-600' : 'text-red-600'
            )}>
              {percentage >= 0 ? '+' : ''}{percentage}%
            </span>
            <span className="text-dark-400">○</span>
          </div>
        )}
      </div>

      <div className="flex items-baseline gap-2 mb-4">
        <span className="text-4xl font-bold">{value}</span>
        {subtitle && (
          <span className="text-dark-500 text-sm">{subtitle}</span>
        )}
      </div>

      {bars && (
        <div className="flex items-end gap-1 h-12">
          {bars.map((val, i) => (
            <div
              key={i}
              className="flex-1 bg-dark-200 rounded-full overflow-hidden"
              style={{ height: '100%' }}
            >
              <div
                className={cn(
                  'w-full rounded-full transition-all duration-500',
                  variant === 'lime' ? 'bg-dark-800' : 'bg-lime-500'
                )}
                style={{ height: `${val * 100}%` }}
              />
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}

// Promo Card (like "Take Your Automation to the Next Level")
interface PromoCardProps {
  title: string;
  buttonText: string;
  onButtonClick?: () => void;
  imageUrl?: string;
}

export function PromoCard({
  title,
  buttonText,
  onButtonClick,
  imageUrl,
}: PromoCardProps) {
  return (
    <Card variant="lime" className="relative overflow-hidden">
      <div className="relative z-10">
        <h3 className="text-xl font-bold mb-4 max-w-[60%]">{title}</h3>
        <button
          onClick={onButtonClick}
          className="flex items-center gap-2 text-sm font-medium hover:underline"
        >
          {buttonText}
          <span>▷</span>
        </button>
      </div>
      {imageUrl && (
        <div className="absolute right-0 bottom-0 w-32 h-32 opacity-80">
          <img src={imageUrl} alt="" className="w-full h-full object-cover rounded-2xl" />
        </div>
      )}
    </Card>
  );
}
