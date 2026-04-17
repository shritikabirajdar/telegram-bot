# Shritika — AI Telegram Bot

Your personal AI assistant on Telegram, built and maintained by **shritika_bot**.

---

## Features

- Smart conversational AI
- Remembers conversation history per user
- `/clear` command to reset conversation
- Customizable personality via system prompt
- Docker-ready for easy deployment

---

## Quick Start

### 1. Get your API keys

**Telegram bot token:**
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the prompts
3. Copy the token it gives you

**AI API key:**
1. Go to https://console.anthropic.com
2. Create an account and go to API Keys
3. Create a new key and copy it

---

### 2. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/shritika_bot.git
cd shritika_bot
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

```
TELEGRAM_TOKEN=your_telegram_bot_token_here
ANTHROPIC_API_KEY=your_api_key_here
```

---

## Run locally (Python)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

---

## Run with Docker

```bash
docker compose up --build -d
```

View logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

---

## Configuration

All config is via environment variables in your `.env` file:

| Variable | Required | Default | Description |
|---|---|---|---|
| `TELEGRAM_TOKEN` | Yes | — | Your Telegram bot token |
| `ANTHROPIC_API_KEY` | Yes | — | Your API key |
| `SYSTEM_PROMPT` | No | "You are Shritika..." | Bot personality/instructions |
| `MAX_HISTORY` | No | `10` | Message pairs to remember per user |

---

## Customize Shritika's personality

Edit `SYSTEM_PROMPT` in your `.env`:

```
SYSTEM_PROMPT=You are Shritika, a witty and sharp assistant who gives direct answers.
```

---

## Project structure

```
shritika_bot/
├── bot.py              # Main bot code
├── requirements.txt    # Dependencies
├── Dockerfile          # Docker image
├── docker-compose.yml  # Docker Compose config
├── .env.example        # Environment variable template
├── .gitignore
└── README.md
```

---

## Deploy to a server

1. SSH into your VPS (DigitalOcean, AWS, Hetzner, etc.)
2. Install Docker: https://docs.docker.com/engine/install/
3. Clone this repo and create your `.env` file
4. Run `docker compose up -d`

The bot runs in the background and auto-restarts if it crashes.

---

## License

MIT — built by shritika_bot
