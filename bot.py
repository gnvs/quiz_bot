# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import create_table
from handlers import router

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    """Основная функция запуска бота"""
    # Создаем таблицы в базе данных
    await create_table()
    
    # Подключаем роутер с обработчиками
    dp.include_router(router)
    
    print("Бот запущен и готов к работе!")
    print(f"Используйте команду /start для начала")
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())