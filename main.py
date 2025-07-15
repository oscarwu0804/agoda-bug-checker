
from config import GMAIL_ACCOUNT, APP_PASSWORD, TO_EMAIL, cities
import requests, smtplib, schedule, time
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

def send_gmail(subject, body):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_ACCOUNT
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_ACCOUNT, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Gmail 通知已發送")
    except Exception as e:
        print("❌ 發送 Gmail 失敗:", e)

def check_bug_price():
    for city in cities:
        today = datetime.today()
        for offset in range(0, 365, 30):  # 每30天檢查一次
            check_in = today + timedelta(days=offset)
            check_out = check_in + timedelta(days=1)
            url = f"https://www.agoda.com/zh-tw/search?city={city['id']}&checkIn={check_in.date()}&checkOut={check_out.date()}&rooms=1&adults=2&currency=TWD"
            headers = { "User-Agent": "Mozilla/5.0" }
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text, 'html.parser')

            all_prices = []
            hotels = soup.find_all(class_='PropertyCard')
            for hotel in hotels:
                try:
                    price_str = hotel.find(class_='PropertyCard__PriceValue').text.strip()
                    price = int(price_str.replace(',', '').replace('TWD', ''))
                    all_prices.append(price)
                except:
                    continue
            if not all_prices:
                continue

            avg_price = sum(all_prices) / len(all_prices)
            found = []
            for hotel in hotels:
                try:
                    name = hotel.find(class_='PropertyCard__HotelName').text.strip()
                    price_str = hotel.find(class_='PropertyCard__PriceValue').text.strip()
                    price = int(price_str.replace(',', '').replace('TWD', ''))
                    if price < avg_price * 0.5 and not any(w in name.lower() for w in ['hostel', 'capsule']):
                        found.append(f"🚨 Bug 價警報\n國家/城市: {city['country']} / {city['name']}\n飯店名稱: {name}\n入住日期: {check_in.date()}\n價格: {price} TWD")
                except:
                    continue
            for msg in found:
                send_gmail("Agoda Bug 價警報", msg)

schedule.every(30).minutes.do(check_bug_price)

while True:
    schedule.run_pending()
    time.sleep(1)
