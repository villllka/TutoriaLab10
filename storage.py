import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("bookings.json")


def load_bookings():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Не удалось прочитать файл бронирований")
        return []


def save_bookings(bookings):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(bookings, file, ensure_ascii=False, indent=2)
