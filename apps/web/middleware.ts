import createMiddleware from 'next-intl/middleware';
import { locales } from './i18n';

export default createMiddleware({
  locales,
  defaultLocale: 'ua',
  localePrefix: 'always',
});

export const config = {
  matcher: ['/', '/(ua|pl)/:path*'],
};
