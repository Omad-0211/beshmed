from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from services.services import WORKERS, getCategory, getTeacher




def main_menu():
    categories = getCategory()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = []
    for idx, category in enumerate(categories, start=1):
        name = category.get("name")
        if name:
            button_text = f"{name}"
            buttons.append(KeyboardButton(button_text))

    keyboard.add(*buttons) 

    return keyboard

    
    
back_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("🔙 Ortga"))

def get_people_buttons(category):
    teachers = getTeacher()  
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton(
            text=teacher['name'], 
            callback_data=f"{category}:{teacher['name']}"
        ) for teacher in teachers
    ]
    
    keyboard.add(*buttons)
    return keyboard