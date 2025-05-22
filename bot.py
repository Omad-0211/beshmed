import os
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import Config
from state.state import ReportStates
from services.services import WORKERS, getTeacher, createUser, getUser


# Botni ishga tushiramiz
bot = Bot(token=Config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Kategoriyalar
category_map = {
    "Korrupsiya holatlari bo'yicha": "korrupsiya",
    "Dars mashg'ulotlarini o'tilishi": "darslar",
    "Nazorat ishlarining olib borilishi": "nazorat",
    "Ishlab chiqarish amaliyoti holati": "ishlabchiqarish",
    "Diplom oldi amaliyot holati": "diploma",
    "Yakuniy davlat attestatsiyasi": "attestatsiya",
    "Amaliy mashg'ulotlar tashkillanish holati": "amaliyot",
    "Ta'lim sifatini yaxshilash bo'yicha": "ta'lim_sifati"
}

SPECIAL_CATEGORIES = [
    "Korrupsiya holatlari bo'yicha",
    "Dars mashg'ulotlarini o'tilishi",
    "Nazorat ishlarining olib borilishi"
]


# Asosiy menyu
main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
for category in category_map.keys():
    main_menu.insert(KeyboardButton(category))

back_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("🔙 Ortga"))





@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    
    user_id = message.from_user.id
    name = message.from_user.first_name
    
    user = getUser(user_id)
    if not user:
        users = {
            "user_id": user_id,
            "name": name
        }
        createUser(users)
        
    await message.reply("Assalomu alaykum! Quyidagi bo'limlardan birini tanlang:", reply_markup=main_menu)




@dp.message_handler(lambda message: message.text and any(message.text.lower().strip().startswith(k.lower()) for k in SPECIAL_CATEGORIES))
async def process_special_category(message: types.Message):
    text = message.text.lower().strip()
    matched_category = None
    for cat in SPECIAL_CATEGORIES:
        if text.startswith(cat.lower()):
            matched_category = cat
            break

    if matched_category:
        category = category_map.get(matched_category)
        teachers = getTeacher()
        keyboard = InlineKeyboardMarkup(row_width=2)
        for teacher in teachers:
            keyboard.add(InlineKeyboardButton(text=teacher['name'], callback_data=f"{category}:{teacher['name']}"))
        await message.answer("Kim haqida izoh bermoqchisiz?", reply_markup=keyboard)
    else:
        await message.reply("Noto'g'ri tanlov.", reply_markup=main_menu)


@dp.callback_query_handler(lambda c: ':' in c.data)
async def process_person_selection(callback_query: types.CallbackQuery, state: FSMContext):
    category, person = callback_query.data.split(":", 1)
    await state.update_data(category=category, person=person)
    await bot.send_message(callback_query.from_user.id, f"✍️ {person} haqida izoh yozing:", reply_markup=back_button)
    await ReportStates.waiting_for_comment.set()




@dp.message_handler(lambda message: message.text and any(message.text.lower().strip().startswith(k.lower()) for k in category_map.keys()) and
                                   not any(message.text.lower().strip().startswith(k.lower()) for k in SPECIAL_CATEGORIES))
async def process_regular_category(message: types.Message, state: FSMContext):
    text = message.text.lower().strip()
    matched_category = None
    for cat in category_map.keys():
        if text.startswith(cat.lower()) and cat not in SPECIAL_CATEGORIES:
            matched_category = cat
            break

    if not matched_category:
        await message.reply("Noto'g'ri tanlov.", reply_markup=main_menu)
        return
    
    category = category_map.get(matched_category)
    await state.update_data(category=category, person=matched_category)
    
    prompt_messages = {
        "Ishlab chiqarish amaliyoti holati": "✍️ Uslubiy rahbar FIOsini yozing:",
        "Diplom oldi amaliyot holati": "✍️ Diplom oldi amaliyot holati bo'yicha izohingizni yozing:",
        "Yakuniy davlat attestatsiyasi": "✍️ Imtihon oluvchining FIOsini kiriting:",
        "Amaliy mashg'ulotlar tashkillanish holati": "✍️ Amaliyot o'qituvchisi FIOsini kiriting:",
        "Ta'lim sifatini yaxshilash bo'yicha": "✍️ Ta'lim sifatini yaxshilash bo'yicha taklifingizni yozing:"
    }
    
    await message.answer(
        prompt_messages.get(matched_category, f"✍️ {matched_category} bo'yicha izohingizni yozing:"),
        reply_markup=back_button
    )
    await ReportStates.waiting_for_comment.set()


@dp.message_handler(state=ReportStates.waiting_for_comment)
async def process_comment(message: types.Message, state: FSMContext):
    if message.text == "🔙 Ortga":
        await message.reply("Bosh menyu", reply_markup=main_menu)
        await state.finish()
        return

    data = await state.get_data()
    username = message.from_user.username or "Anonim"
    
    channel_text = (
        f"📢 Yangi izoh!\n"
        f"🏷 Kategoriya: {data['category']}\n"
        f"👤 Shaxs: {data.get('person', 'Noma\'lum')}\n"
        f"👨‍💻 Foydalanuvchi: @{username}\n"
        f"📝 Izoh: {message.text}\n"
        f"📅 Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    try:
        await bot.send_message(Config.CHANNEL_ID, channel_text)
        await message.reply("✅ Izohingiz qabul qilindi!", reply_markup=main_menu)
    except Exception as e:
        await message.reply("❌ Kanalga yuborishda xatolik yuz berdi.", reply_markup=main_menu)
    
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
