from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from services.services import WORKERS

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_menu.add(
    KeyboardButton("Korrupsiya holatlari bo'yicha"),
    KeyboardButton("Dars mashg'ulotlarini o'tilishi"),
    KeyboardButton("Nazorat ishlarining olib borilishi"),
    KeyboardButton("Ishlab chiqarish amaliyoti holati"),
    KeyboardButton("Diplom oldi amaliyot holati"),
    KeyboardButton("Yakuniy davlat attestatsiyasi"),
),
main_menu.add(
    KeyboardButton("Amaliy mashg'ulotlar tashkillanish holati"),
    KeyboardButton("Ta'lim sifatini yaxshilash bo'yicha"),
)

back_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("🔙 Ortga"))

def get_people_buttons(category):
    workers = WORKERS.get(category, [])
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=name, callback_data=f"{category}:{name}") for name in workers]
    keyboard.add(*buttons)
    return keyboard