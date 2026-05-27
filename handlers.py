# handlers.py
from aiogram import types, F
from aiogram.filters.command import Command
from aiogram import Router
from datetime import datetime

from database import (
    get_quiz_index, update_quiz_index, save_quiz_result,
    get_user_last_result, get_top_scores
)
from keyboards import generate_options_keyboard, get_main_keyboard
from questions import QUIZ_DATA, get_question_count

router = Router()

async def get_question(message: types.Message, user_id: int):
    """Отправляет текущий вопрос пользователю"""
    current_question_index = await get_quiz_index(user_id)
    
    if current_question_index >= len(QUIZ_DATA):
        await message.answer("Квиз завершен!")
        return
    
    question_data = QUIZ_DATA[current_question_index]
    
    # Сохраняем ответ пользователя в чат
    await message.answer(
        f"*Вопрос {current_question_index + 1} из {len(QUIZ_DATA)}:*\n\n"
        f"{question_data['question']}",
        parse_mode="Markdown",
        reply_markup=generate_options_keyboard(question_data['options'])
    )

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    username = message.from_user.username or message.from_user.first_name
    await message.answer(
        f"*Привет, {username}!*\n\n"
        "Добро пожаловать в *Python Quiz Bot*!\n\n"
        "Я помогу тебе проверить знания Python.\n\n"
        "*Команды:*\n"
        "• /quiz или 'Начать квиз' - начать тестирование\n"
        "• /progress или 'Мой прогресс' - показать прогресс\n"
        "• /top или 'Топ игроков' - рейтинг игроков\n"
        "• /help или 'Помощь' - справка\n\n"
        "Готов проверить свои знания? Нажми 'Начать квиз'!",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

@router.message(Command("help"))
@router.message(F.text == "ℹ️ Помощь")
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = (
        "*Справка по использованию бота*\n\n"
        "*Доступные команды:*\n"
        "• `/start` - начать работу с ботом\n"
        "• `/quiz` - начать новый квиз\n"
        "• `/progress` - посмотреть свой прогресс\n"
        "• `/top` - топ игроков\n"
        "• `/help` - показать эту справку\n\n"
        "*Как играть:*\n"
        "1. Нажми 'Начать квиз'\n"
        "2. Отвечай на вопросы, выбирая вариант\n"
        "3. После ответа покажется правильный вариант\n"
        "4. В конце узнаешь свой результат!\n\n"
        "*Особенности:*\n"
        "• Бот сохраняет твой прогресс\n"
        "• Можно прервать и продолжить позже\n"
        "• Результаты сохраняются в таблицу лидеров\n\n"
        "_Удачи в прохождении квиза!_"
    )
    await message.answer(help_text, parse_mode="Markdown")

@router.callback_query(lambda c: c.data.startswith('answer_'))
async def handle_answer(callback: types.CallbackQuery):
    """Обработчик ответов на вопросы"""
    answer_index = int(callback.data.split('_')[1])
    user_id = callback.from_user.id
    username = callback.from_user.username or callback.from_user.first_name
    
    current_question_index = await get_quiz_index(user_id)
    
    # Проверяем, не завершен ли уже квиз
    if current_question_index >= len(QUIZ_DATA):
        await callback.message.answer("Квиз уже завершен! Начните новый с помощью /quiz")
        await callback.answer()
        return
    
    question_data = QUIZ_DATA[current_question_index]
    is_correct = (answer_index == question_data['correct_option'])
    
    # Удаляем кнопки
    await callback.bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    # Выводим результат в чат
    if is_correct:
        response = f"*Верно!*\n\n{question_data['explanation']}"
    else:
        correct_answer = question_data['options'][question_data['correct_option']]
        response = (
            f"*Неправильно*\n\n"
            f"Правильный ответ: *{correct_answer}*\n\n"
            f"*Пояснение:* {question_data['explanation']}"
        )
    
    await callback.message.answer(response, parse_mode="Markdown")
    
    # Обновляем индекс вопроса
    next_question_index = current_question_index + 1
    await update_quiz_index(user_id, next_question_index, username, callback.from_user.first_name)
    
    # Проверяем завершение квиза
    if next_question_index >= len(QUIZ_DATA):
        # Сохраняем результат
        score = await calculate_score(user_id)
        await save_quiz_result(user_id, username, score, len(QUIZ_DATA))
        
        last_result = await get_user_last_result(user_id)
        if last_result:
            score, total, percentage, date = last_result
            await callback.message.answer(
                f"*Поздравляем! Вы завершили квиз!* 🎉\n\n"
                f"*Ваш результат:*\n"
                f"Правильных ответов: {score}/{total}\n"
                f"Процент: {percentage:.1f}%\n\n"
                f"Чтобы начать заново, нажмите 'Начать квиз'",
                parse_mode="Markdown"
            )
        else:
            await callback.message.answer(
                "Поздравляем! Вы завершили квиз!\n"
                "Нажмите 'Начать квиз' чтобы пройти снова"
            )
    else:
        await get_question(callback.message, user_id)
    
    await callback.answer()

async def calculate_score(user_id: int) -> int:
    """Вычисляет количество правильных ответов пользователя"""
    # Простой подсчет - можно расширить для хранения всех ответов
    # Здесь возвращаем заглушку, в реальном приложении нужно хранить все ответы
    return 0  # TODO: реализовать подсчет правильных ответов

@router.message(Command("quiz"))
@router.message(F.text == "Начать квиз")
async def cmd_quiz(message: types.Message):
    """Обработчик начала квиза"""
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Сбрасываем прогресс
    await update_quiz_index(user_id, 0, username, message.from_user.first_name)
    
    await message.answer(
        "*Начинаем квиз по Python!*\n\n"
        "У тебя будет 10 вопросов. Удачи!",
        parse_mode="Markdown"
    )
    await get_question(message, user_id)

@router.message(Command("progress"))
@router.message(F.text == "Мой прогресс")
async def show_progress(message: types.Message):
    """Показывает прогресс пользователя"""
    user_id = message.from_user.id
    current_index = await get_quiz_index(user_id)
    total = len(QUIZ_DATA)
    last_result = await get_user_last_result(user_id)
    
    if current_index >= total:
        progress_text = "*Квиз завершен!*\n\n"
    else:
        progress_text = f"*Текущий прогресс:*\n"
        progress_text += f"Вопрос {current_index + 1} из {total}\n"
        progress_text += f"Завершено: {(current_index/total)*100:.1f}%\n\n"
    
    # Добавляем последний результат
    if last_result:
        score, total_q, percentage, date = last_result
        date_obj = datetime.fromisoformat(date)
        progress_text += (
            f"*Последний результат:*\n"
            f"Правильно: {score}/{total_q}\n"
            f"Процент: {percentage:.1f}%\n"
            f"Дата: {date_obj.strftime('%d.%m.%Y %H:%M')}"
        )
    else:
        progress_text += "*Вы еще не проходили квиз*\nНажмите 'Начать квиз'!"
    
    await message.answer(progress_text, parse_mode="Markdown")

@router.message(Command("top"))
@router.message(F.text == "Топ игроков")
async def show_top(message: types.Message):
    """Показывает топ игроков"""
    top_scores = await get_top_scores(10)
    
    if not top_scores:
        await message.answer("Пока нет результатов. Будьте первым, кто пройдет квиз!")
        return
    
    top_text = "*Топ игроков по результатам квиза:*\n\n"
    
    for i, (username, score, total, percentage, date) in enumerate(top_scores, 1):
        medal = {1: "", 2: "", 3: ""}.get(i, "")
        name = username or f"Player_{i}"
        top_text += f"{medal} *{i}. {name}* - {percentage:.1f}% ({score}/{total})\n"
    
    top_text += "\n_Пройдите квиз, чтобы попасть в топ!_"
    
    await message.answer(top_text, parse_mode="Markdown")