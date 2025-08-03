
---

## 4. 🛠 config.py

```python
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 20))
TRADERS_FILE = os.getenv("TRADERS_FILE", "traders.json")
