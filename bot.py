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

@dp.message_handler(lambda message: message.text in category_map.keys())
async def process_category(message: types.Message):
    category = category_map.get(message.text)
    if category:
        await message.answer("Kim haqida izoh bermoqchisiz?", reply_markup=get_people_buttons(category))
    else:
        await message.reply("Noto'g'ri tanlov. Iltimos, menyudan biror bo'limni tanlang.", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "Ta'lim sifatini yaxshilash bo'yicha")
async def handle_talim_sifati(message: types.Message):
    user_states[message.from_user.id] = {
        "category": "ta'lim_sifati",
        "person": "Ta'lim sifatini yaxshilash"
    }
    await message.answer("✍️ Ta'lim sifatini yaxshilash bo'yicha taklifingizni yozing:", reply_markup=back_button)

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