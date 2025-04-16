import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

CITY_URL = "https://sinoptik.ua/погода-київ"
DB_NAME = "weather.db"
SLEEP_TIME = 1800

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            datetime TEXT,
            temperature TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_temperature():
    response = requests.get(CITY_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    temp_div = soup.find('p', class_='today-temp')
    if temp_div:
        return temp_div.text.strip()
    else:
        raise ValueError("Не вдалося знайти температуру")

def insert_data(temp):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO weather (datetime, temperature) VALUES (?, ?)", (now, temp))
    conn.commit()
    conn.close()

def main():
    create_db()
    print("⏳ Початок збору даних про погоду... Натисніть Ctrl+C для зупинки.")
    try:
        while True:
            try:
                temp = get_temperature()
                insert_data(temp)
                print(f"✅ Дані збережено: {datetime.now()} — {temp}")
            except Exception as e:
                print(f"⚠️ Помилка при отриманні температури: {e}")
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        print("\n🛑 Збір даних зупинено вручну.")

if __name__ == "__main__":
    main()
