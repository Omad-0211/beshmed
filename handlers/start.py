from aiogram import types
from utils.buttons import main_menu

async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum! Quyidagi bo'limlardan birini tanlang:", reply_markup=main_menu())