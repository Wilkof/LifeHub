import { notFound } from 'next/navigation';
import { getRequestConfig } from 'next-intl/server';

export const locales = ['ua', 'pl'] as const;
export type Locale = (typeof locales)[number];

export const localeNames: Record<Locale, string> = {
  ua: 'Українська',
  pl: 'Polski',
};

export default getRequestConfig(async ({ locale }) => {
  if (!locales.includes(locale as Locale)) notFound();

  return {
    messages: (await import(`./messages/${locale}.json`)).default,
  };
});
