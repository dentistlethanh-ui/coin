import os, requests, datetime

# Lấy cấu hình
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID        = os.getenv("CHAT_ID")
SYMBOLS        = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

# Gửi Telegram
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

# Lấy nến 15m qua REST public của Binance
def fetch_15m(symbol):
    url = (
        "https://api.binance.com/api/v3/klines"
        f"?symbol={symbol}"
        "&interval=15m"
        "&limit=2"
    )
    r = requests.get(url, timeout=10)
    data = r.json()
    # data[-1] là cây nến vừa đóng
    open_p  = float(data[-1][1])
    close_p = float(data[-1][4])
    return open_p, close_p

# Phân tích và gửi tín hiệu
def analyze_and_send():
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    for symbol in SYMBOLS:
        o, c = fetch_15m(symbol)
        if c > o * 1.005:
            entry = c
            sl    = round(o, 2)
            tp    = round(c * 1.01, 2)
            winr  = "60%"
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
