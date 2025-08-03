import os, requests, datetime
from binance.client import Client

# Lấy cấu hình từ GitHub Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID        = os.getenv("CHAT_ID")
SYMBOLS        = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]  # Sửa danh sách coin của bạn

# Hàm gửi tin nhắn lên Telegram
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

# Lấy nến 15m từ Binance (public API)
def fetch_15m(symbol):
    client = Client()
    klines = client.get_klines(
        symbol=symbol,
        interval=Client.KLINE_INTERVAL_15MINUTE,
        limit=2
    )
    open_p, close_p = float(klines[-1][1]), float(klines[-1][4])
    return open_p, close_p

# Phân tích và gửi tín hiệu
def analyze_and_send():
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    for symbol in SYMBOLS:
        o, c = fetch_15m(symbol)
        # Ví dụ điều kiện LONG: giá đóng cửa cao hơn giá mở hơn 0.5%
        if c > o * 1.005:
            entry = c
            sl    = round(o, 2)
            tp    = round(c * 1.01, 2)
            winr  = "60%"  # Tỉ lệ thành công ước tính
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
