import { ReactNode } from 'react';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { locales, type Locale } from '@/i18n';
import Sidebar from '@/app/components/layout/Sidebar';
import '@/app/globals.css';

interface LocaleLayoutProps {
  children: ReactNode;
  params: { locale: string };
}

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({
  children,
  params: { locale },
}: LocaleLayoutProps) {
  // Validate locale
  if (!locales.includes(locale as Locale)) {
    notFound();
  }

  // Get messages for the current locale
  const messages = await getMessages();

  return (
    <html lang={locale}>
      <head>
        <title>LifeHub - Your Personal Dashboard</title>
        <meta name="description" content="Personal life management dashboard" />
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className="bg-sage-300 min-h-screen">
        <NextIntlClientProvider messages={messages}>
          <div className="flex">
            {/* Sidebar */}
            <Sidebar locale={locale} />

            {/* Main Content */}
            <main className="flex-1 ml-20 min-h-screen p-6">
              {children}
            </main>
          </div>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
