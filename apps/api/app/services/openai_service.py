"""OpenAI service for AI assistant."""
from typing import Optional
import json
from openai import AsyncOpenAI

from app.config import settings


class OpenAIService:
    """Service for OpenAI API interactions."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        
        self.system_prompts = {
            "general": """Ти - персональний AI асистент у дашборді LifeHub. Допомагаєш з плануванням, продуктивністю та організацією життя.
Відповідай українською мовою. Будь конкретним і практичним. Уникай банальних порад та мотиваційних цитат.
Враховуй контекст користувача (задачі, цілі, звички, здоров'я) для персоналізованих відповідей.""",
            
            "plan_day": """Ти - експерт з планування та продуктивності. Створюєш оптимальні денні плани.
Враховуй: пріоритети задач, рівень енергії протягом дня, дедлайни, важливість перерв.
Давай конкретні часові блоки та послідовність. Українською мовою.""",
            
            "break_goal": """Ти - коуч з досягнення цілей. Розбиваєш великі цілі на конкретні кроки.
Використовуй SMART підхід. Визначай milestones та key results.
Будь практичним і реалістичним. Українською мовою.""",
            
            "week_summary": """Ти - аналітик особистої продуктивності. Аналізуєш дані за тиждень.
Знаходиш патерни, сильні та слабкі сторони. Даєш actionable рекомендації.
Не критикуй, а підтримуй та спрямовуй. Українською мовою.""",
            
            "anti_procrastination": """Ти - експерт з подолання прокрастинації. Допомагаєш почати діяти прямо зараз.
Фокусуйся на: перший мікро-крок, зниження бар'єру входу, негайна дія.
Будь енергійним але не нав'язливим. Українською мовою.""",
            
            "daily_briefing": """Ти - персональний асистент, що готує ранковий брифінг.
Коротко, по суті, мотивуюче. Фокус на найважливішому.
Персональна мотивація без банальних цитат. Українською мовою.""",
            
            "motivation": """Генеруй персоналізовані мотиваційні повідомлення.
НЕ використовуй відомі цитати чи банальності.
Звертайся напряму до користувача. Будь автентичним. Українською мовою."""
        }
    
    async def chat(
        self,
        message: str,
        mode: str = "general",
        context: Optional[dict] = None
    ) -> str:
        """Send message to OpenAI and get response."""
        if not self.client:
            return "AI асистент недоступний. Налаштуйте OPENAI_API_KEY."
        
        system_prompt = self.system_prompts.get(mode, self.system_prompts["general"])
        
        # Add context to system prompt
        if context:
            context_str = f"\n\nКонтекст користувача:\n{json.dumps(context, ensure_ascii=False, indent=2)}"
            system_prompt += context_str
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",  # Cost-effective model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Помилка AI: {str(e)}"
    
    async def generate_motivation(self, context: Optional[dict] = None) -> str:
        """Generate personalized motivation message."""
        prompt = "Створи коротке (2-3 речення) персональне мотиваційне повідомлення на ранок."
        return await self.chat(prompt, mode="motivation", context=context)
    
    async def generate_evening_reflection(self, context: dict) -> str:
        """Generate evening reflection prompt."""
        prompt = """На основі даних про сьогоднішній день, створи:
1. Коротке визнання того, що вдалось
2. Один конструктивний висновок
3. Перший крок на завтра"""
        return await self.chat(prompt, mode="general", context=context)


# Dependency
def get_openai_service() -> OpenAIService:
    """Get OpenAI service instance."""
    return OpenAIService()
