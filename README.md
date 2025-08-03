# hyperliquid-monitor
hyperliquid-monitor
# Hyperliquid 多地址监听 & Telegram 推送

项目用于监听 Hyperliquid 上多个地址的仓位变化及挂单 / 委托状态，并推送信息到 Telegram。

## 配置

- `traders.json`：地址–备注对应列表
- 环境变量：
  - `TELEGRAM_TOKEN`：Telegram Bot Token
  - `TELEGRAM_CHAT_ID`：聊天或群组 ID

## 启动方式

```bash
pip install -r requirements.txt
python hyperliquid_monitor.py
