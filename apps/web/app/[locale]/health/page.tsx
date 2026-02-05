'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import { cn, moodEmojis } from '@/app/lib/utils';
import {
  Moon,
  Droplets,
  Smile,
  Zap,
  Plus,
  Minus,
  TrendingUp,
} from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

export default function HealthPage({ params: { locale } }: PageProps) {
  const t = useTranslations('health');
  const [todayData, setTodayData] = useState({
    sleep_hours: 7.5,
    sleep_quality: 4,
    water_glasses: 5,
    mood: 4,
    energy: 3,
  });

  const addWater = () => {
    setTodayData((prev) => ({
      ...prev,
      water_glasses: Math.min(prev.water_glasses + 1, 20),
    }));
  };

  const removeWater = () => {
    setTodayData((prev) => ({
      ...prev,
      water_glasses: Math.max(prev.water_glasses - 1, 0),
    }));
  };

  const setMood = (mood: number) => {
    setTodayData((prev) => ({ ...prev, mood }));
  };

  return (
    <div className="max-w-4xl">
      <Header locale={locale} title={t('title')} />

      <div className="grid grid-cols-2 gap-6">
        {/* Sleep Card */}
        <Card className="col-span-2 md:col-span-1">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 rounded-2xl bg-indigo-100 flex items-center justify-center">
              <Moon className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h3 className="font-semibold">{t('sleep')}</h3>
              <p className="text-sm text-dark-500">Цієї ночі</p>
            </div>
          </div>

          <div className="text-center mb-6">
            <div className="text-5xl font-bold">{todayData.sleep_hours}</div>
            <div className="text-dark-500">{t('hours')}</div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-3">{t('sleepQuality')}</label>
            <div className="flex justify-between">
              {[1, 2, 3, 4, 5].map((quality) => (
                <button
                  key={quality}
                  onClick={() =>
                    setTodayData((prev) => ({ ...prev, sleep_quality: quality }))
                  }
                  className={cn(
                    'w-12 h-12 rounded-xl flex items-center justify-center text-2xl transition-all',
                    todayData.sleep_quality === quality
                      ? 'bg-indigo-500 text-white'
                      : 'bg-indigo-50 hover:bg-indigo-100'
                  )}
                >
                  {quality}
                </button>
              ))}
            </div>
          </div>
        </Card>

        {/* Water Card */}
        <Card className="col-span-2 md:col-span-1">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 rounded-2xl bg-cyan-100 flex items-center justify-center">
              <Droplets className="w-6 h-6 text-cyan-600" />
            </div>
            <div>
              <h3 className="font-semibold">{t('water')}</h3>
              <p className="text-sm text-dark-500">Сьогодні</p>
            </div>
          </div>

          <div className="text-center mb-6">
            <div className="text-5xl font-bold">{todayData.water_glasses}</div>
            <div className="text-dark-500">/ 8 склянок</div>
          </div>

          {/* Water progress */}
          <div className="flex justify-center gap-1 mb-6">
            {Array.from({ length: 8 }, (_, i) => (
              <div
                key={i}
                className={cn(
                  'w-8 h-10 rounded-lg transition-colors',
                  i < todayData.water_glasses ? 'bg-cyan-400' : 'bg-cyan-100'
                )}
              />
            ))}
          </div>

          <div className="flex justify-center gap-4">
            <button
              onClick={removeWater}
              className="w-12 h-12 rounded-xl bg-dark-100 flex items-center justify-center hover:bg-dark-200"
            >
              <Minus className="w-5 h-5" />
            </button>
            <button
              onClick={addWater}
              className="w-12 h-12 rounded-xl bg-cyan-500 text-white flex items-center justify-center hover:bg-cyan-600"
            >
              <Plus className="w-5 h-5" />
            </button>
          </div>
        </Card>

        {/* Mood Card */}
        <Card className="col-span-2 md:col-span-1">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 rounded-2xl bg-amber-100 flex items-center justify-center">
              <Smile className="w-6 h-6 text-amber-600" />
            </div>
            <div>
              <h3 className="font-semibold">{t('mood')}</h3>
              <p className="text-sm text-dark-500">Як себе почуваєш?</p>
            </div>
          </div>

          <div className="flex justify-between">
            {[1, 2, 3, 4, 5].map((mood) => (
              <button
                key={mood}
                onClick={() => setMood(mood)}
                className={cn(
                  'w-14 h-14 rounded-2xl flex items-center justify-center text-3xl transition-all',
                  todayData.mood === mood
                    ? 'bg-amber-400 scale-110'
                    : 'bg-amber-50 hover:bg-amber-100'
                )}
              >
                {moodEmojis[mood as keyof typeof moodEmojis]}
              </button>
            ))}
          </div>

          <div className="text-center mt-4 text-dark-500">
            {t(`moods.${todayData.mood}`)}
          </div>
        </Card>

        {/* Energy Card */}
        <Card className="col-span-2 md:col-span-1">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 rounded-2xl bg-green-100 flex items-center justify-center">
              <Zap className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h3 className="font-semibold">{t('energy')}</h3>
              <p className="text-sm text-dark-500">Рівень енергії</p>
            </div>
          </div>

          <div className="flex justify-between">
            {[1, 2, 3, 4, 5].map((energy) => (
              <button
                key={energy}
                onClick={() =>
                  setTodayData((prev) => ({ ...prev, energy }))
                }
                className={cn(
                  'flex-1 h-20 mx-1 rounded-xl flex items-end justify-center pb-2 transition-all',
                  todayData.energy >= energy
                    ? 'bg-green-400'
                    : 'bg-green-100'
                )}
              >
                <span
                  className={cn(
                    'font-bold',
                    todayData.energy >= energy ? 'text-white' : 'text-green-400'
                  )}
                >
                  {energy}
                </span>
              </button>
            ))}
          </div>
        </Card>

        {/* Weekly Stats */}
        <Card className="col-span-2">
          <div className="flex items-center gap-3 mb-6">
            <TrendingUp className="w-5 h-5 text-dark-500" />
            <h3 className="font-semibold">Статистика за тиждень</h3>
          </div>

          <div className="grid grid-cols-4 gap-4">
            <div className="text-center p-4 bg-indigo-50 rounded-2xl">
              <div className="text-2xl font-bold text-indigo-600">7.2</div>
              <div className="text-sm text-dark-500">Сер. сон (год)</div>
            </div>
            <div className="text-center p-4 bg-cyan-50 rounded-2xl">
              <div className="text-2xl font-bold text-cyan-600">42</div>
              <div className="text-sm text-dark-500">Всього води</div>
            </div>
            <div className="text-center p-4 bg-amber-50 rounded-2xl">
              <div className="text-2xl font-bold text-amber-600">3.8</div>
              <div className="text-sm text-dark-500">Сер. настрій</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-2xl">
              <div className="text-2xl font-bold text-green-600">7</div>
              <div className="text-sm text-dark-500">Днів залоговано</div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
