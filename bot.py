import os
import json
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, bot
from handlers.start import send_welcome
from state.state import user_states
from services.services import save_report
from utils.buttons import main_menu, back_button, get_people_buttons
from utils.texts import category_map

CHANNEL_ID = -1002468881091  # Kanal ID (-100...)

# Ismlar ro'yxati chiqadigan maxsus kategoriyalar
SPECIAL_CATEGORIES = [
    "Dars mashg'ulotlarini o'tilishi",
    "Nazorat ishlarining olib borilishi",
    "Korrupsiya holatlari bo'yicha"
]

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum! Quyidagi bo'limlardan birini tanlang:", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text in SPECIAL_CATEGORIES)
async def process_special_category(message: types.Message):
    category = category_map.get(message.text)
    if category:
        await message.answer("Kim haqida izoh bermoqchisiz?", reply_markup=get_people_buttons(category))
    else:
        await message.reply("Noto'g'ri tanlov. Iltimos, menyudan biror bo'limni tanlang.", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text in category_map.keys() and message.text not in SPECIAL_CATEGORIES)
async def process_direct_category(message: types.Message):
    category = category_map.get(message.text)
    if not category:
        await message.reply("Noto'g'ri tanlov. Iltimos, menyudan biror bo'limni tanlang.", reply_markup=main_menu)
        return

    # Maxsus yo'nalishlar uchun mos xabarlar
    prompt_messages = {
        "Yakuniy davlat attestatsiyasi": "✍️ Imtihon oluvchining FIOsini kiriting:",
        "Ishlab chiqarish amaliyoti holati": "✍️ Uslubiy rahbar FIOsini yozing:",
        "Amaliy mashg'ulotlar tashkillanish holati": "✍️ Amaliyot o'qituvchisi FIOsini kiriting:",
        "Diplom oldi amaliyot holati": "✍️ Diplom oldi amaliyot holati bo'yicha izohingizni yozing:",
        "Ta'lim sifatini yaxshilash bo'yicha": "✍️ Ta'lim sifatini yaxshilash bo'yicha taklifingizni yozing:"
    }

    user_states[message.from_user.id] = {
        "category": category,
        "person": message.text
    }
    
    await message.answer(prompt_messages.get(message.text, f"✍️ {message.text} bo'yicha izohingizni yozing:"), 
                        reply_markup=back_button)

@dp.callback_query_handler(lambda c: ':' in c.data)
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    category, person = callback_query.data.split(":", 1)
    user_states[user_id] = {
        "category": category,
        "person": person
    }
    await bot.send_message(user_id, f"✍️ {person} haqida izoh yozing:", reply_markup=back_button)

@dp.message_handler(lambda message: message.text == "🔙 Ortga")
async def back_to_menu(message: types.Message):
    if message.from_user.id in user_states:
        del user_states[message.from_user.id]
    await message.answer("Bosh menyu", reply_markup=main_menu)

@dp.message_handler(content_types=['text'])
async def process_text(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    if user_id in user_states:
        data = user_states[user_id]
        success, saved_data = await save_report(
            data["category"], 
            data["person"], 
            message.text, 
            user_id,
            username
        )
        
        if success:
            await message.reply("✅ Izohingiz qabul qilindi!", reply_markup=main_menu)
            
            channel_text = (
                f"📢 Yangi izoh!\n"
                f"🏷 Kategoriya: *{data['category'].replace('_',' ').title()}*\n"
                f"👤 Shaxs: {data['person']}\n"
                f"👨‍💻 Foydalanuvchi: @{username if username else 'Anonim'}\n"
                f"📝 Izoh: {message.text}\n"
                f"📅 Vaqt: {saved_data['timestamp']}"
            )
            try:
                await bot.send_message(CHANNEL_ID, channel_text, parse_mode="Markdown")
            except Exception as e:
                print(f"Kanalga yuborishda xato: {e}")
        else:
            await message.reply("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.", reply_markup=main_menu)
        del user_states[user_id]
    else:
        await message.reply("Iltimos, menyudan kerakli bo'limni tanlang.", reply_markup=main_menu)

from aiohttp import ClientSession

async def on_shutdown(dp):
    await bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    session = await ClientSession().__aexit__()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)