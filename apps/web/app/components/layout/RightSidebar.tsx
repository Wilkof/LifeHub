'use client';

import { useTranslations } from 'next-intl';
import {
  Users,
  GraduationCap,
  HelpCircle,
  Building2,
  FileText,
  BarChart3,
  ArrowUpRight,
} from 'lucide-react';

const quickLinks = [
  { key: 'community', icon: Users },
  { key: 'academy', icon: GraduationCap },
  { key: 'helpCenter', icon: HelpCircle },
  { key: 'partners', icon: Building2 },
  { key: 'blog', icon: FileText },
  { key: 'useCases', icon: BarChart3 },
];

export default function RightSidebar() {
  const tSidebar = useTranslations('sidebar');

  return (
    <aside className="w-72 bg-sage-200/50 rounded-3xl p-4 space-y-3">
      <div className="grid grid-cols-2 gap-3">
        {/* Community */}
        <div className="card bg-white/80 p-4 cursor-pointer hover:bg-white transition-colors">
          <Users className="w-5 h-5 mb-2 text-dark-600" />
          <div className="text-sm font-medium">Community</div>
          <ArrowUpRight className="w-4 h-4 text-dark-400 absolute top-3 right-3" />
        </div>

        {/* Academy */}
        <div className="card bg-white/80 p-4 cursor-pointer hover:bg-white transition-colors">
          <GraduationCap className="w-5 h-5 mb-2 text-dark-600" />
          <div className="text-sm font-medium">Academy</div>
          <ArrowUpRight className="w-4 h-4 text-dark-400 absolute top-3 right-3" />
        </div>
      </div>

      {/* List items */}
      {[
        { icon: HelpCircle, title: 'Help Center', desc: 'Explore our detailed documentatio...' },
        { icon: Building2, title: 'Partner Directory', desc: 'Find the perfect partner to suppor...' },
        { icon: FileText, title: 'Blog', desc: 'Access popular guides & stories ab...' },
        { icon: BarChart3, title: 'Use Cases', desc: 'Get inspired by all the ways you ca...' },
      ].map((item, i) => (
        <div
          key={i}
          className="flex items-start gap-3 p-3 rounded-2xl bg-white/60 hover:bg-white cursor-pointer transition-colors"
        >
          <div className="w-10 h-10 rounded-xl bg-dark-100 flex items-center justify-center flex-shrink-0">
            <item.icon className="w-5 h-5 text-dark-600" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="font-medium text-sm">{item.title}</div>
            <div className="text-xs text-dark-500 truncate">{item.desc}</div>
          </div>
          <ArrowUpRight className="w-4 h-4 text-dark-400 flex-shrink-0" />
        </div>
      ))}
    </aside>
  );
}
