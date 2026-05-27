# database.py
import aiosqlite
from config import DB_NAME

async def create_table():
    """Создает таблицы в базе данных"""
    async with aiosqlite.connect(DB_NAME) as db:
        # Таблица для сохранения прогресса
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY, 
                question_index INTEGER,
                username TEXT,
                first_name TEXT
            )
        ''')
        
        # Таблица для сохранения результатов
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                score INTEGER,
                total_questions INTEGER,
                percentage REAL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        await db.commit()

async def get_quiz_index(user_id):
    """Получает текущий индекс вопроса пользователя"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            'SELECT question_index FROM quiz_state WHERE user_id = ?', 
            (user_id,)
        ) as cursor:
            results = await cursor.fetchone()
            return results[0] if results else 0

async def update_quiz_index(user_id, index, username="", first_name=""):
    """Обновляет индекс вопроса пользователя"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR REPLACE INTO quiz_state (user_id, question_index, username, first_name) 
            VALUES (?, ?, ?, ?)
        ''', (user_id, index, username, first_name))
        await db.commit()

async def save_quiz_result(user_id, username, score, total):
    """Сохраняет результат прохождения квиза"""
    percentage = (score / total) * 100
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO quiz_results (user_id, username, score, total_questions, percentage)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, score, total, percentage))
        await db.commit()

async def get_user_last_result(user_id):
    """Получает последний результат пользователя"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('''
            SELECT score, total_questions, percentage, date 
            FROM quiz_results 
            WHERE user_id = ? 
            ORDER BY date DESC 
            LIMIT 1
        ''', (user_id,)) as cursor:
            return await cursor.fetchone()

async def get_top_scores(limit=10):
    """Получает лучшие результаты"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('''
            SELECT username, score, total_questions, percentage, date 
            FROM quiz_results 
            ORDER BY percentage DESC 
            LIMIT ?
        ''', (limit,)) as cursor:
            return await cursor.fetchall()