import requests
import time
import json
import os
import telegram

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TRADERS_FILE = "traders.json"
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 20))

bot = telegram.Bot(token=TELEGRAM_TOKEN)
last_positions = {}
last_orders = {}

def load_traders():
    with open(TRADERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_position(addr):
    r = requests.get(f"https://api.hyperliquid.xyz/info?user={addr}", timeout=10)
    return r.json().get("position", {}) if r.ok else {}

def get_open_orders(addr):
    r = requests.get(f"https://api.hyperliquid.xyz/user/open_orders?user={addr}", timeout=10)
    return r.json() if r.ok else []

def send_message(text):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

def format_position_msg(name, pos, prev):
    size = pos.get("size", 0)
    prev_size = prev.get("size", 0) if prev else 0
    change = "📈 加仓" if size > prev_size else ("📉 减仓" if size < prev_size else "平仓")
    side = "多单" if pos.get("side") == "long" else "空单"
    return (f"📊 [{name}] 仓位更新\n方向：{side}\n仓位：{size}\n杠杆：{pos.get('leverage')}x\n"
            f"开仓价：{pos.get('entry_price')}\n爆仓价：{pos.get('liquidation_price')}\n"
            f"当前PNL：{pos.get('pnl')}\n变动类型：{change}")

def format_order_msg(name, orders):
    msgs = []
    for o in orders:
        side = "买入" if o.get("side") == "buy" else "卖出"
        msgs.append(f"📋 [{name}] 新挂单\n方向：{side}\n价格：{o.get('price')}\n数量：{o.get('size')}\n类型：{o.get('order_type')}")
    return "\n".join(msgs)

def loop_once(traders):
    for addr, name in traders.items():
        pos = get_position(addr)
        prev = last_positions.get(addr)
        if pos and pos != prev:
            send_message(format_position_msg(name, pos, prev))
            last_positions[addr] = pos

        orders = get_open_orders(addr)
        prev_ids = {o.get("oid") for o in last_orders.get(addr, [])}
        cur_ids = {o.get("oid") for o in orders}
        if cur_ids != prev_ids:
            send_message(format_order_msg(name, orders))
            last_orders[addr] = orders

def main():
    traders = load_traders()
    while True:
        try:
            loop_once(traders)
            time.sleep(POLL_INTERVAL)
        except Exception as e:
            print("Error:", e)
            time.sleep(30)

if __name__ == "__main__":
    main()
