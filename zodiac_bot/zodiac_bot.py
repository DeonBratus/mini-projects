import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import random
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)
bot = Bot(token="")
dp = Dispatcher(bot=bot)

# Словарь для хранения знаков зодиака пользователей
user_zodiac_signs = {}
users_id = []

zodiac_signs = [
    "♈ Овен", "♉ Телец", "♊ Близнецы", "♋ Рак",
    "♌ Лев", "♍ Дева", "♎ Весы", "♏ Скорпион",
    "♐ Стрелец", "♑ Козерог", "♒ Водолей", "♓ Рыбы"
]

zodiac_info = {
    "♈ Овен": "Описание Овна...\n Это овен, и это овен, а овен это овен",
    "♉ Телец": "Описание Тельца...",
    "♊ Близнецы": "Описание Близнецов...",
    "♋ Рак": "Описание Рака...",
    "♌ Лев": "Описание Льва...",
    "♍ Дева": "Описание Девы...", 
    "♎ Весы": "Описание Весов...", 
    "♏ Скорпион": "Описание Скорпиона...",
    "♐ Стрелец": "Описание Стрельца...", 
    "♑ Козерог": "Описание Козерога...", 
    "♒ Водолей": "Описание Водолея...", 
    "♓ Рыбы": "Описание Рыб..."
}

daily_horoscopes = [
    "Сегодня отличный день для новых начинаний!",
    "Ожидаются интересные встречи.",
    "Время для саморазвития и новых проектов.",
    "Стоит больше внимания уделить своим близким.",
    "Не забудьте про отдых и заботу о себе.",
    "Ваши идеи найдут поддержку окружающих."
]


# Keyboards for zodiac signs
zodiacs_sign_buttons = [[KeyboardButton(text=sign) for sign in zodiac_signs[i:i+4]] for i in range(0, 12, 4)]
zodiac_kb_markup = ReplyKeyboardMarkup(keyboard=zodiacs_sign_buttons, resize_keyboard=True)

# Button for update of keyboard
inline_button_update = [[InlineKeyboardButton(text="Обновить", callback_data="update_horoscope")]]
inline_murkup_update = InlineKeyboardMarkup(inline_keyboard=inline_button_update)


# Hadler for start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Выберите свой знак зодиака:",
        reply_markup=zodiac_kb_markup
    )


# Main hadnlder for sending of message about horoscope
async def horoscope_update(message: types.Message):

    sign = user_zodiac_signs[message.from_user.id]

    if sign in zodiac_info:
        user_zodiac_signs[message.from_user.id] = sign
        
        if message.from_user.id in users_id:
            users_id.append(message.from_user.id)

        current_date = datetime.now().strftime("%Y-%m-%d")
        zodiac_image_path = "https://cs14.pikabu.ru/post_img/2023/05/18/8/1684412732156192750.jpg"
        
        text_msg = (
            f"Ваш знак - {sign}.\nПредсказание! На <b>{current_date}</b>\n"
            f"{random.choice(daily_horoscopes)}"
            )

        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=zodiac_image_path,
            caption=text_msg,
            reply_markup=inline_murkup_update,
            parse_mode="HTML"
        )


# Handler for /update msg info about horoscope
@dp.message(Command("update"))
async def cmd_update(message: types.Message):
    await horoscope_update(message=message)


# Callback for inline button "update"
@dp.callback_query(F.data == "update_horoscope")
async def callback_update_hs(message: types.Message):
    await horoscope_update(message=message)

# Handler from zodiac keyboards
@dp.message()
async def change_zodiac(message: types.Message):

    msg_text = message.text

    if msg_text in zodiac_info:
        user_zodiac_signs[message.from_user.id] = msg_text

        if message.from_user.id not in users_id:
            users_id.append(message.from_user.id)

        await message.answer(
            text=f'{zodiac_info[msg_text]}',
            reply_markup=types.ReplyKeyboardRemove()
            )
            
        await horoscope_update(message=message)
        
    elif msg_text == "/change_zodiac":
        await message.answer(
            "Выберите свой знак зодиака:", 
            reply_markup=zodiac_kb_markup
            )
    else:
        await message.answer("Извините, я не понял. Пожалуйста, выберите свой знак зодиака.")


# handler of sending msg everyday
async def everyday_update_horoscope():
    for user_id in users_id:
        if user_id in user_zodiac_signs:
            sign = user_zodiac_signs[user_id]
            await bot.send_message(
                user_id,
                f"Ваш знак зодиака: {sign}\n" + random.choice(daily_horoscopes))


# Clear handler - just delete all msgs
@dp.message(Command("clear"))
async def cmd_clear_history(message: types.Message):
    for msg_id in range(message.message_id, 0, -1):
        await bot.delete_message(message.from_user.id, msg_id)


# main handler, using schduler for planning of sending msg
async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(everyday_update_horoscope, trigger="cron", hour=10, minute=0)  # Ежедневная отправка в 10:00
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
