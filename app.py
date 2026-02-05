from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- CẤU HÌNH ---
TELEGRAM_TOKEN = "PASTE_TOKEN_CUA_BAN_VAO_DAY"
CHAT_ID = "PASTE_CHAT_ID_VAO_DAY"  # Ví dụ: "-100123456789"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML" # Để tô đậm, nghiêng được
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Lỗi gửi tin: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
    
    # Format tin nhắn gửi về Tele
    # Giả sử TradingView gửi JSON: {"symbol": "BTCUSDT", "action": "BUY", "price": 96000, "sl": 95000, "tp": 98000}
    
    symbol = data.get('symbol', 'UNKNOWN')
    action = data.get('action', 'ALERT')
    price = data.get('price', '0')
    sl = data.get('sl', '0')
    tp = data.get('tp', '0')
    vol = data.get('vol', '')
    
    # Icon cho sinh động
    icon = "🟢" if action == "BUY" or action == "LONG" else "🔴"
    
    msg_content = (
        f"<b>{icon} TÍN HIỆU MỚI: {symbol}</b>\n"
        f"---------------------------\n"
        f"🔹 <b>Action:</b> {action}\n"
        f"🔹 <b>Entry:</b> {price}\n"
        f"🔹 <b>Volume:</b> {vol}\n"
        f"🔻 <b>SL:</b> {sl}\n"
        f"🚀 <b>TP:</b> {tp}\n"
        f"---------------------------\n"
        f"<i>Bot System by UITer</i>"
    )
    
    send_telegram_message(msg_content)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
