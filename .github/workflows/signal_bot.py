import os, requests, datetime
from binance.client import Client

# 1. Cấu hình bằng GitHub Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID        = os.getenv("CHAT_ID")
SYMBOLS        = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]  # Thay bằng danh sách của bạn

# 2. Hàm gửi tin nhắn Telegram
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

# 3. Lấy dữ liệu nến 15m từ Binance REST API
def fetch_15m(symbol):
    client = Client()  # không cần API key cho public klines
    klines = client.get_klines(symbol=symbol,
                               interval=Client.KLINE_INTERVAL_15MINUTE,
                               limit=2)
    # klines[-1] là cây nến vừa đóng
    open_p, close_p = float(klines[-1][1]), float(klines[-1][4])
    return open_p, close_p

# 4. Logic tín hiệu đơn giản (ví dụ: close > open ⇒ LONG)
def analyze_and_send():
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    for symbol in SYMBOLS:
        o, c = fetch_15m(symbol)
        # Ví dụ điều kiện LONG: tăng >0.5%
        if c > o * 1.005:
            entry = c
            sl    = round(o, 2)
            tp    = round(c * 1.01, 2)
            winr  = "60%"  # bạn có thể thay bằng công thức tính win rate
            text  = (
                f"[15m] {now}\n"
                f"{symbol} – LONG\n"
                f"Entry: {entry:.2f}\n"
                f"SL: {sl:.2f}\n"
                f"TP: {tp:.2f}\n"
                f"WinRate: {winr}"
            )
            send_telegram(text)

if __name__ == "__main__":
    analyze_and_send()
