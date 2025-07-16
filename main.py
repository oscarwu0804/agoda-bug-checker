from config import GMAIL_ACCOUNT, APP_PASSWORD, TO_EMAIL, cities
import requests, smtplib, schedule, time, traceback
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

print("✅ Worker 已啟動，準備開始執行任務")

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
        print(f"❌ 發送 Gmail 失敗: {e}")
        traceback.print_exc()

def check_bug_price():
    print("🔍 正在檢查 Agoda …")
    for city in cities:
        today = datetime.today()
        for offset in range(0, 365, 30):  # 每30天檢查一次
            check_in = today + timedelta(days=offset)
            check_out = check_in + timedelta(days=1)
            url = f"https://www.agoda.com/zh-tw/search?city={city['id']}&checkIn={check_in.date()}&checkOut={check_out.date()}&rooms=1&adults=2&currency=TWD"
            headers = { "User-Agent": "Mozilla/5.0" }
            print(f"🌐 抓取網址: {url}")
            try:
                resp = requests.get(url, headers=headers, timeout=15)
                print(f"📄 回應狀態碼: {resp.status_code}")
                soup = BeautifulSoup(resp.text, 'html.parser')

                hotels = soup.find_all(class_='PropertyCard')
                print(f"🏨 找到飯店卡片數量: {len(hotels)}")
                all_prices = []
                for hotel in hotels:
                    try:
                        name = hotel.find(class_='PropertyCard__HotelName').text.strip()
                        price_str = hotel.find(class_='PropertyCard__PriceValue').text.strip()
                        price = int(price_str.replace(',', '').replace('TWD', ''))
                        all_prices.append(price)
                        print(f"🏨 {name} - {price} TWD")
                    except:
                        print("⚠️ 無法解析某個飯店價格")
                        continue
                if not all_prices:
                    print(f"⚠️ {city['name']} 沒有找到任何價格")
                    continue

                avg_price = sum(all_prices) / len(all_prices)
                print(f"💰 {city['name']} 平均價格: {avg_price:.0f} TWD")

                found = []
                for hotel in hotels:
                    try:
                        name = hotel.find(class_='PropertyCard__HotelName').text.strip()
                        price_str = hotel.find(class_='PropertyCard__PriceValue').text.strip()
                        price = int(price_str.replace(',', '').replace('TWD', ''))
                        if price < avg_price * 0.8:
                            msg_text = (f"🚨 Bug 價警報\n國家/城市: {city['country']} / {city['name']}\n"
                                        f"飯店名稱: {name}\n入住日期: {check_in.date()}\n價格: {price} TWD")
                            found.append(msg_text)
                            print(f"🚨 發現疑似 Bug 價: {name} - {price} TWD")
                    except:
                        continue
                for msg in found:
                    send_gmail("Agoda Bug 價警報", msg)

            except Exception as e:
                print(f"❌ 抓取 {city['name']} 網頁失敗: {e}")
                traceback.print_exc()

schedule.every(1).minutes.do(check_bug_price)  # 驗證版：每 1 分鐘跑一次

while True:
    schedule.run_pending()
    time.sleep(1)

