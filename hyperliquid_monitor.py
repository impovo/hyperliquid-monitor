import time
import json
import requests
import telegram
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, POLL_INTERVAL, TRADERS_FILE
from logger import logger

bot = telegram.Bot(token=TELEGRAM_TOKEN)
last_positions = {}
last_orders = {}

def load_traders():
    with open(TRADERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_position(addr):
    try:
        r = requests.get(f"https://api.hyperliquid.xyz/info?user={addr}", timeout=10)
        r.raise_for_status()
        return r.json().get("position", {})
    except Exception as e:
        logger.error(f"获取仓位失败 {addr}: {e}")
        return {}

def get_open_orders(addr):
    try:
        r = requests.get(f"https://api.hyperliquid.xyz/user/open_orders?user={addr}", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.error(f"获取挂单失败 {addr}: {e}")
        return []

def send_message(text):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"发送消息失败: {e}")

def format_position_msg(name, pos, prev):
    size = pos.get("size", 0)
    prev_size = prev.get("size", 0) if prev else 0
    change = "📈 加仓" if size > prev_size else ("📉 减仓" if size < prev_size else "✅ 平仓")
    side = "多单" if pos.get("side") == "long" else "空单"
    return (f"*[{name}]* 仓位更新\n"
            f"方向：{side}    仓位：{size}\n"
            f"杠杆：{pos.get('leverage')}x    开仓价：{pos.get('entry_price')}\n"
            f"爆仓价：{pos.get('liquidation_price')}    当前PNL：{pos.get('pnl')}\n"
            f"变动类型：{change}")

def format_order_msg(name, orders):
    lines = []
    for o in orders:
        side = "买入" if o.get("side")=="buy" else "卖出"
        lines.append(f"*[{name}]* 新挂单\n方向：{side} 价格：{o.get('price')}  数量：{o.get('size')}  类型：{o.get('order_type')}")
    return "\n".join(lines)

def loop_once(traders):
    for addr, name in traders.items():
        pos = get_position(addr)
        if pos and pos != last_positions.get(addr):
            send_message(format_position_msg(name, pos, last_positions.get(addr)))
            last_positions[addr] = pos
        orders = get_open_orders(addr)
        prev_ids = {o.get("oid") for o in last_orders.get(addr, [])}
        cur_ids = {o.get("oid") for o in orders}
        if cur_ids != prev_ids:
            send_message(format_order_msg(name, orders))
            last_orders[addr] = orders

def main():
    traders = load_traders()
    logger.info(f"开始监听 {len(traders)} 个地址")
    while True:
        try:
            loop_once(traders)
            time.sleep(POLL_INTERVAL)
        except Exception as e:
            logger.error(f"主循环异常: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
