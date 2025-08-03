# Hyperliquid Monitor - 多地址监听 & Telegram 推送

## 功能
- 监听多个地址的仓位变化（size, leverage, entry_price, liquidation_price, pnl）
- 监控挂单状态变化（委托新增/取消）
- 支持地址备注（traders.json）
- 推送消息至 Telegram Bot

## 配置
- `traders.json`：填写地址–备注对照表
- 环境变量：
  - `TELEGRAM_TOKEN`
  - `TELEGRAM_CHAT_ID`
  - 可选：`POLL_INTERVAL`（轮询秒数，默认 20）

## 部署
```bash
pip install -r requirements.txt
python hyperliquid_monitor.py
