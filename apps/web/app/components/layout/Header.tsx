'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useTranslations } from 'next-intl';
import { cn } from '@/app/lib/utils';
import { locales, localeNames, type Locale } from '@/i18n';
import { Settings, Plus, Globe } from 'lucide-react';

interface HeaderProps {
  locale: string;
  title?: string;
}

export default function Header({ locale, title }: HeaderProps) {
  const [showLangMenu, setShowLangMenu] = useState(false);
  const pathname = usePathname();
  const t = useTranslations('common');

  const switchLocale = (newLocale: Locale) => {
    const pathWithoutLocale = pathname.replace(`/${locale}`, '');
    window.location.href = `/${newLocale}${pathWithoutLocale}`;
  };

  return (
    <header className="flex items-center justify-between mb-8">
      {/* Title */}
      <div>
        <h1 className="text-3xl font-bold text-dark-900">
          {title || t('appName')}
        </h1>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3">
        {/* Language Switcher */}
        <div className="relative">
          <button
            onClick={() => setShowLangMenu(!showLangMenu)}
            className="w-10 h-10 rounded-xl bg-white flex items-center justify-center hover:bg-dark-100 transition-colors"
          >
            <Globe className="w-5 h-5 text-dark-600" />
          </button>

          {showLangMenu && (
            <div className="absolute right-0 top-12 bg-white rounded-xl shadow-card p-2 min-w-[140px] z-50">
              {locales.map((loc) => (
                <button
                  key={loc}
                  onClick={() => {
                    switchLocale(loc);
                    setShowLangMenu(false);
                  }}
                  className={cn(
                    'w-full text-left px-3 py-2 rounded-lg text-sm transition-colors',
                    locale === loc
                      ? 'bg-lime-100 text-lime-800 font-medium'
                      : 'hover:bg-dark-100'
                  )}
                >
                  {localeNames[loc]}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Settings */}
        <Link
          href={`/${locale}/settings`}
          className="w-10 h-10 rounded-xl bg-white flex items-center justify-center hover:bg-dark-100 transition-colors"
        >
          <Settings className="w-5 h-5 text-dark-600" />
        </Link>

        {/* Create Button */}
        <button className="btn btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" />
          <span>Create a New Scenario</span>
        </button>
      </div>
    </header>
  );
}
