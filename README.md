# 🚀 LifeHub - Personal Life Management Dashboard

**LifeHub** — персональний дашборд для повного контролю над життям. Управління задачами, фінансами, здоров'ям, звичками, цілями та нотатками в одному місці.

![LifeHub Dashboard](./docs/screenshot.png)

## ✨ Можливості

### 📊 Dashboard
- Огляд дня: MIT (Most Important Tasks), події, звички
- Погода та швидка статистика
- AI-згенерований ранковий брифінг

### ✅ Tasks & Planning
- Задачі з пріоритетами та дедлайнами
- MIT (3 найважливіші задачі дня)
- Статуси: Backlog → Todo → In Progress → Done
- Теги та проєкти

### 📅 Calendar
- Тижневий/місячний вигляд
- Події з нагадуваннями
- Експорт/імпорт iCal

### 💰 Finances
- Доходи та витрати
- Бюджети по категоріях
- Підписки з нагадуваннями
- Аналітика витрат

### 🏃 Health
- Трекінг сну (години + якість)
- Вода (склянки)
- Настрій (1-5)
- Автоматичні алерти

### 🎯 Habits
- Щоденні звички
- Streak tracking
- Гнучка частота

### 🚀 Goals
- Короткострокові та довгострокові цілі
- Прогрес у відсотках
- Milestones та Key Results

### 📝 Notes & Journal
- Нотатки та щоденник
- Інбокс думок
- Теги та папки

### 🤖 AI Assistant
- Інтеграція з GPT
- Режими: план дня, розбивка цілі, підсумок тижня
- Антипрокрастинаційні поради

### 🔔 Автоматизації (Telegram)
- Ранковий брифінг (08:00)
- Денне нагадування (13:00)
- Вечірній чек-ін (21:30)
- Нагадування про дедлайни
- Тижневий огляд

---

## 🛠 Tech Stack

| Компонент | Технологія |
|-----------|------------|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS |
| **Backend** | FastAPI (Python), SQLAlchemy |
| **Database** | PostgreSQL |
| **AI** | OpenAI GPT API |
| **Bot** | python-telegram-bot |
| **i18n** | next-intl (UA/PL) |
| **Deploy** | Netlify (frontend), Render (backend + DB) |

---

## 📁 Структура проєкту

```
lifehub/
├── apps/
│   ├── api/                    # FastAPI Backend
│   │   ├── app/
│   │   │   ├── main.py         # FastAPI app
│   │   │   ├── config.py       # Configuration
│   │   │   ├── database.py     # DB connection
│   │   │   ├── models/         # SQLAlchemy models
│   │   │   ├── schemas/        # Pydantic schemas
│   │   │   ├── routers/        # API endpoints
│   │   │   └── services/       # Business logic
│   │   ├── requirements.txt
│   │   ├── Procfile            # Render start command
│   │   └── render.yaml         # Render config
│   │
│   └── web/                    # Next.js Frontend
│       ├── app/
│       │   ├── [locale]/       # i18n routes
│       │   ├── components/     # UI components
│       │   └── lib/            # Utilities
│       ├── messages/           # i18n translations
│       ├── package.json
│       └── netlify.toml        # Netlify config
│
└── packages/
    └── shared/                 # Shared types (v2)
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- PostgreSQL
- OpenAI API Key
- Telegram Bot Token

### 1. Clone repository
```bash
git clone https://github.com/your-username/lifehub.git
cd lifehub
```

### 2. Backend Setup
```bash
cd apps/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp env.example .env
# Edit .env with your values:
# - DATABASE_URL
# - OPENAI_API_KEY
# - TELEGRAM_BOT_TOKEN
# - APP_ACCESS_TOKEN

# Run migrations (creates tables)
python -c "from app.database import init_db; init_db()"

# Start server
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd apps/web

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start dev server
npm run dev
```

### 4. Open in browser
```
http://localhost:3000
```

---

## 📦 Deployment

### Backend → Render.com

1. **Create Web Service:**
   - Go to [render.com](https://render.com) → New → Web Service
   - Connect GitHub repo
   - Root Directory: `apps/api`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker`

2. **Create PostgreSQL:**
   - New → PostgreSQL
   - Copy Internal Database URL

3. **Environment Variables:**
   ```
   APP_ENV=production
   APP_ACCESS_TOKEN=<generate-secure-token>
   DATABASE_URL=<postgres-url-from-step-2>
   OPENAI_API_KEY=<your-openai-key>
   TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
   WEATHER_API_KEY=<openweathermap-key>
   FRONTEND_URL=https://your-app.netlify.app
   TIMEZONE=Europe/Warsaw
   ```

### Frontend → Netlify

1. **Connect to Netlify:**
   - Go to [netlify.com](https://netlify.com) → Add new site → Import from Git
   - Connect GitHub repo

2. **Build Settings:**
   - Base directory: `apps/web`
   - Build command: `npm run build`
   - Publish directory: `apps/web/.next`

3. **Environment Variables:**
   ```
   NEXT_PUBLIC_API_URL=https://your-api.onrender.com
   ```

4. **Install Next.js plugin:**
   - Go to Plugins → Search "@netlify/plugin-nextjs" → Install

---

## 🤖 Telegram Bot Setup

1. **Create bot via @BotFather:**
   ```
   /newbot
   Name: LifeHub
   Username: lifehub_your_bot
   ```

2. **Copy token and add to backend env:**
   ```
   TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
   ```

3. **Set webhook:**
   ```
   https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-api.onrender.com/api/telegram/webhook
   ```

4. **Start bot:**
   - Open Telegram, find your bot
   - Send `/start` to register
   - Your Chat ID will be saved automatically

### Available Commands
| Command | Description |
|---------|-------------|
| `/start` | Register for notifications |
| `/today` | Show today's tasks |
| `/add <text>` | Add new task |
| `/done <id>` | Complete task |
| `/week` | Weekly summary |
| `/water` | Add water glass |
| `/help` | Show all commands |

---

## 🔐 Security

- **APP_ACCESS_TOKEN**: Simple token-based auth (header: `X-Access-Token`)
- All secrets stored in environment variables
- OpenAI/Telegram keys only on backend
- Rate limiting on AI endpoints

---

## 🌍 Internationalization

Supported languages:
- 🇺🇦 Ukrainian (ua) - default
- 🇵🇱 Polish (pl)

Switch language in the header or via URL:
- `/ua/tasks` → Ukrainian
- `/pl/tasks` → Polish

---

## 📝 API Documentation

After starting the backend:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`
- OpenAPI JSON: `http://localhost:8000/api/openapi.json`

---

## 🗺 Roadmap

### MVP (v1.0) ✅
- [x] Dashboard with all modules
- [x] Tasks, Calendar, Finances, Health, Habits, Goals, Notes
- [x] AI Assistant integration
- [x] Telegram bot + notifications
- [x] i18n (UA/PL)

### v2.0 (Planned)
- [ ] Google Calendar sync
- [ ] Gmail integration (unified inbox)
- [ ] Google Drive file attachment
- [ ] Content planning module (Posts & Ideas)
- [ ] Mobile PWA optimization
- [ ] Dark theme

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 👤 Author

Created with ❤️ for productivity enthusiasts.

**Questions?** Open an issue or reach out!
