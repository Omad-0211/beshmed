# buttons.py fayli
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from services.services import WORKERS

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_menu.add(
    KeyboardButton("Korrupsiya holatlari bo'yicha"),
    KeyboardButton("Dars mashg'ulotlari bo'yicha"),
    KeyboardButton("Nazorat ishlari bo'yicha"),
    KeyboardButton("Ishlab chiqarish amaliyoti bo'yicha"),
    KeyboardButton("Diplom ishlari amaliyoti bo'yicha"),
    KeyboardButton("Yakuniy davlat attestatsiyasi bo'yicha"),
    KeyboardButton("Amaliy mashg'ulotlar tashkili bo'yicha"),
    KeyboardButton("Ta'lim sifatini yaxshilash bo'yicha")
)

back_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("🔙 Ortga"))

def get_people_buttons(category):
    workers = WORKERS.get(category, [])
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=name, callback_data=f"{category}:{name}") for name in workers]
    keyboard.add(*buttons)
    return keyboard