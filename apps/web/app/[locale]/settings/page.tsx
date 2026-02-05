'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import { cn } from '@/app/lib/utils';
import {
  User,
  Globe,
  Bell,
  MessageCircle,
  CloudSun,
  Palette,
  Save,
} from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

export default function SettingsPage({ params: { locale } }: PageProps) {
  const t = useTranslations('settings');
  const [settings, setSettings] = useState({
    name: 'User',
    language: 'ua',
    timezone: 'Europe/Warsaw',
    weather_city: 'Warsaw',
    telegram_chat_id: '',
    telegram_notifications_enabled: true,
    morning_briefing_time: '08:00',
    midday_reminder_time: '13:00',
    evening_checkin_time: '21:30',
    enable_morning_briefing: true,
    enable_midday_reminder: true,
    enable_evening_checkin: true,
    enable_weekly_review: true,
    theme: 'light',
    accent_color: '#c8e972',
  });

  const handleChange = (key: string, value: any) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = () => {
    // TODO: Call API to save settings
    console.log('Saving settings:', settings);
  };

  return (
    <div className="max-w-3xl">
      <Header locale={locale} title={t('title')} />

      <div className="space-y-6">
        {/* Profile Section */}
        <Card>
          <div className="flex items-center gap-3 mb-6">
            <User className="w-5 h-5 text-dark-500" />
            <h2 className="text-lg font-semibold">{t('profile')}</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Ім'я</label>
              <input
                type="text"
                value={settings.name}
                onChange={(e) => handleChange('name', e.target.value)}
                className="input"
              />
            </div>
          </div>
        </Card>

        {/* Language & Timezone */}
        <Card>
          <div className="flex items-center gap-3 mb-6">
            <Globe className="w-5 h-5 text-dark-500" />
            <h2 className="text-lg font-semibold">{t('language')} & {t('timezone')}</h2>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">{t('language')}</label>
              <select
                value={settings.language}
                onChange={(e) => handleChange('language', e.target.value)}
                className="input"
              >
                <option value="ua">Українська</option>
                <option value="pl">Polski</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">{t('timezone')}</label>
              <select
                value={settings.timezone}
                onChange={(e) => handleChange('timezone', e.target.value)}
                className="input"
              >
                <option value="Europe/Warsaw">Europe/Warsaw</option>
                <option value="Europe/Kyiv">Europe/Kyiv</option>
              </select>
            </div>
          </div>
        </Card>

        {/* Telegram */}
        <Card>
          <div className="flex items-center gap-3 mb-6">
            <MessageCircle className="w-5 h-5 text-dark-500" />
            <h2 className="text-lg font-semibold">{t('telegram')}</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Chat ID</label>
              <input
                type="text"
                value={settings.telegram_chat_id}
                onChange={(e) => handleChange('telegram_chat_id', e.target.value)}
                placeholder="Відправте /start боту для отримання Chat ID"
                className="input"
              />
            </div>
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={settings.telegram_notifications_enabled}
                onChange={(e) =>
                  handleChange('telegram_notifications_enabled', e.target.checked)
                }
                className="w-5 h-5 rounded"
              />
              <span>Увімкнути сповіщення в Telegram</span>
            </label>
          </div>
        </Card>

        {/* Notifications Schedule */}
        <Card>
          <div className="flex items-center gap-3 mb-6">
            <Bell className="w-5 h-5 text-dark-500" />
            <h2 className="text-lg font-semibold">{t('notifications')}</h2>
          </div>

          <div className="space-y-4">
            {/* Morning Briefing */}
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium">{t('morningBriefing')}</div>
                <div className="text-sm text-dark-500">
                  Погода, задачі, звички
                </div>
              </div>
              <div className="flex items-center gap-3">
                <input
                  type="time"
                  value={settings.morning_briefing_time}
                  onChange={(e) =>
                    handleChange('morning_briefing_time', e.target.value)
                  }
                  className="input w-28"
                />
                <input
                  type="checkbox"
                  checked={settings.enable_morning_briefing}
                  onChange={(e) =>
                    handleChange('enable_morning_briefing', e.target.checked)
                  }
                  className="w-5 h-5 rounded"
                />
              </div>
            </div>

            {/* Midday Reminder */}
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium">{t('middayReminder')}</div>
                <div className="text-sm text-dark-500">
                  Нагадування про воду та задачі
                </div>
              </div>
              <div className="flex items-center gap-3">
                <input
                  type="time"
                  value={settings.midday_reminder_time}
                  onChange={(e) =>
                    handleChange('midday_reminder_time', e.target.value)
                  }
                  className="input w-28"
                />
                <input
                  type="checkbox"
                  checked={settings.enable_midday_reminder}
                  onChange={(e) =>
                    handleChange('enable_midday_reminder', e.target.checked)
                  }
                  className="w-5 h-5 rounded"
                />
              </div>
            </div>

            {/* Evening Check-in */}
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium">{t('eveningCheckin')}</div>
                <div className="text-sm text-dark-500">
                  Підсумок дня, план на завтра
                </div>
              </div>
              <div className="flex items-center gap-3">
                <input
                  type="time"
                  value={settings.evening_checkin_time}
                  onChange={(e) =>
                    handleChange('evening_checkin_time', e.target.value)
                  }
                  className="input w-28"
                />
                <input
                  type="checkbox"
                  checked={settings.enable_evening_checkin}
                  onChange={(e) =>
                    handleChange('enable_evening_checkin', e.target.checked)
                  }
                  className="w-5 h-5 rounded"
                />
              </div>
            </div>

            {/* Weekly Review */}
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium">{t('weeklyReview')}</div>
                <div className="text-sm text-dark-500">
                  Огляд тижня (неділя)
                </div>
              </div>
              <input
                type="checkbox"
                checked={settings.enable_weekly_review}
                onChange={(e) =>
                  handleChange('enable_weekly_review', e.target.checked)
                }
                className="w-5 h-5 rounded"
              />
            </div>
          </div>
        </Card>

        {/* Weather */}
        <Card>
          <div className="flex items-center gap-3 mb-6">
            <CloudSun className="w-5 h-5 text-dark-500" />
            <h2 className="text-lg font-semibold">{t('weather')}</h2>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">{t('city')}</label>
            <input
              type="text"
              value={settings.weather_city}
              onChange={(e) => handleChange('weather_city', e.target.value)}
              className="input"
            />
          </div>
        </Card>

        {/* Save Button */}
        <button
          onClick={handleSave}
          className="btn btn-primary w-full flex items-center justify-center gap-2"
        >
          <Save className="w-4 h-4" />
          Зберегти налаштування
        </button>
      </div>
    </div>
  );
}
