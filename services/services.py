import os
import json
from datetime import datetime
from aiogram import Bot

# Faqat 3 ta kategoriya uchun ismlar ro'yxati
WORKERS = {
    "korrupsiya": [
        "Rahmonov Alisher", "Usmonov Sardor", "Adminstratorlar bo'limi", 
        "Xolisov Farrux", "Karimov Jahongir", "Toshmatov Shoxrux",
        "Qodirov Laziz", "Yuldashev Bobur", "Komilov Islom", "Nazarov Doniyor"
    ],
    "darslar": [
        "Rahmonov Alisher", "Usmonov Sardor", "Adminstratorlar bo'limi", 
        "Xolisov Farrux", "Karimov Jahongir", "Toshmatov Shoxrux",
        "Qodirov Laziz", "Yuldashev Bobur", "Komilov Islom", "Nazarov Doniyor"
    ], 
    "nazorat": [
        "Rahmonov Alisher", "Usmonov Sardor", "Adminstratorlar bo'limi", 
        "Xolisov Farrux", "Karimov Jahongir", "Toshmatov Shoxrux",
        "Qodirov Laziz", "Yuldashev Bobur", "Komilov Islom", "Nazarov Doniyor"
    ]
}

REPORT_FILES = {
    "korrupsiya": "data/korrupsiya.json",
    "darslar": "data/darslar.json",
    "nazorat": "data/nazorat.json",
    "ishlabchiqarish": "data/ishlabchiqarish.json",
    "diploma": "data/diploma.json",
    "attestatsiya": "data/attestatsiya.json",
    "amaliyot": "data/amaliyot.json",
    "ta'lim_sifati": "data/talim_sifati.json"
}

async def save_report(category, person, message_text, user_id, username):
    data = {
        "person": person,
        "message": message_text,
        "user_id": user_id,
        "username": username if username else "Anonim",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    os.makedirs("data", exist_ok=True)
    file_path = REPORT_FILES.get(category)
    if not file_path:
        return False, None

    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, "r", encoding='utf-8') as f:
                reports = json.load(f)
        else:
            reports = []

        reports.append(data)

        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(reports, f, indent=4, ensure_ascii=False)
        return True, data
    except Exception as e:
        print(f"Xato: {e}")
        await Bot.get_current().send_message(user_id, f"❌ Xatolik yuz berdi: {e}")
        return False, None