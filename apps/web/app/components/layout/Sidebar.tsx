'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useTranslations } from 'next-intl';
import { cn } from '@/app/lib/utils';
import {
  LayoutDashboard,
  CheckSquare,
  Calendar,
  Wallet,
  Heart,
  Target,
  FileText,
  Bot,
  BarChart3,
  Settings,
  HelpCircle,
  Users,
  Sparkles,
  Link as LinkIcon,
  Plus,
  Repeat,
} from 'lucide-react';

interface SidebarProps {
  locale: string;
}

const mainNavItems = [
  { key: 'today', icon: LayoutDashboard, href: '' },
  { key: 'tasks', icon: CheckSquare, href: '/tasks' },
  { key: 'calendar', icon: Calendar, href: '/calendar' },
  { key: 'finances', icon: Wallet, href: '/finances' },
  { key: 'health', icon: Heart, href: '/health' },
  { key: 'habits', icon: Repeat, href: '/habits' },
  { key: 'goals', icon: Target, href: '/goals' },
  { key: 'notes', icon: FileText, href: '/notes' },
  { key: 'ai', icon: Bot, href: '/ai' },
  { key: 'analytics', icon: BarChart3, href: '/analytics' },
  { key: 'settings', icon: Settings, href: '/settings' },
];

export default function Sidebar({ locale }: SidebarProps) {
  const pathname = usePathname();
  const t = useTranslations('nav');
  const tSidebar = useTranslations('sidebar');
  const [isHovered, setIsHovered] = useState(false);

  const isActive = (href: string) => {
    const basePath = `/${locale}${href}`;
    if (href === '') {
      return pathname === `/${locale}` || pathname === `/${locale}/`;
    }
    return pathname.startsWith(basePath);
  };

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 h-screen bg-dark-900 text-white z-50',
        'flex flex-col transition-all duration-300 ease-in-out',
        isHovered ? 'w-64' : 'w-20'
      )}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Logo */}
      <div className="flex items-center justify-center h-20 border-b border-dark-700">
        <div className="w-10 h-10 rounded-xl bg-lime-500 flex items-center justify-center">
          <Plus className="w-6 h-6 text-dark-900 rotate-45" />
        </div>
        {isHovered && (
          <span className="ml-3 font-bold text-xl animate-fade-in">LifeHub</span>
        )}
      </div>

      {/* Main Navigation */}
      <nav className="flex-1 py-6 px-3 space-y-1 overflow-y-auto">
        {mainNavItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.href);

          return (
            <Link
              key={item.key}
              href={`/${locale}${item.href}`}
              className={cn(
                'sidebar-item',
                active && 'active'
              )}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              {isHovered && (
                <span className="animate-fade-in whitespace-nowrap">
                  {t(item.key)}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Bottom Section */}
      <div className="p-3 border-t border-dark-700 space-y-1">
        {isHovered ? (
          <>
            <div className="sidebar-item">
              <HelpCircle className="w-5 h-5 flex-shrink-0" />
              <div className="animate-fade-in">
                <div className="text-sm">{tSidebar('helpCenter')}</div>
                <div className="text-xs text-dark-400">{tSidebar('helpDesc')}</div>
              </div>
            </div>
            <div className="sidebar-item">
              <Users className="w-5 h-5 flex-shrink-0" />
              <span className="animate-fade-in">{tSidebar('community')}</span>
            </div>
          </>
        ) : (
          <>
            <div className="sidebar-item justify-center">
              <HelpCircle className="w-5 h-5" />
            </div>
            <div className="sidebar-item justify-center">
              <Users className="w-5 h-5" />
            </div>
          </>
        )}
      </div>

      {/* User Avatar */}
      <div className="p-4 border-t border-dark-700">
        <div className={cn(
          'flex items-center',
          isHovered ? 'justify-start' : 'justify-center'
        )}>
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-lime-400 to-lime-600 flex items-center justify-center font-bold text-dark-900">
            U
          </div>
          {isHovered && (
            <span className="ml-3 animate-fade-in font-medium">User</span>
          )}
        </div>
      </div>
    </aside>
  );
}
