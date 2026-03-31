# GoodMarket

A Web3 earning platform built on the GoodDollar ecosystem. Users earn G$ tokens on the Celo network through educational quizzes, social media tasks, minigames, and community engagement.

## Tech Stack

- **Backend:** Python 3.12, Flask, Gunicorn (gthread workers)
- **Frontend:** Server-side rendered Jinja2 templates with static assets
- **Database:** Supabase (PostgreSQL)
- **Blockchain:** Web3.py, Celo network, GoodDollar (G$) contracts
- **WalletConnect:** Node.js sidecar service (`wc_service.js`) using `@walletconnect/sign-client`
- **Package Manager (Python):** uv (with `uv.lock` and `pyproject.toml`)
- **Package Manager (Node):** npm (`package.json`)

## Project Layout

| Path | Description |
|------|-------------|
| `main.py` | Flask app entry point, initializes all services and blueprints |
| `routes.py` | Core API routes and auth decorators |
| `blockchain.py` | Blockchain logic (UBI claims, G$ balances) |
| `config.py` | Global configuration and reward settings |
| `supabase_client.py` | Database connection and utilities |
| `gunicorn.conf.py` | Gunicorn server configuration (port 5000, 0.0.0.0) |
| `wc_service.js` | Node.js WalletConnect service (runs on port 3001) |
| `learn_and_earn/` | Learn & Earn quiz module |
| `minigames/` | Minigames module |
| `twitter_task/` | Twitter social task module |
| `telegram_task/` | Telegram social task module |
| `discourse_task/` | Discourse forum task module |
| `community_stories/` | Community stories module |
| `jumble/` | Jumble word game module |
| `price_prediction/` | Price prediction module |
| `referral_program/` | Referral program module |
| `contracts/` | Solidity smart contracts and deployment scripts |
| `static/` | Static assets (JS bundles, icons, manifest) |
| `templates/` | Jinja2 HTML templates |

## Workflow

- **Start application:** `uv run gunicorn --config gunicorn.conf.py main:app`
- Runs on port **5000** (0.0.0.0)
- WalletConnect sidecar runs on port **3001** (started automatically by main.py if `WALLETCONNECT_PROJECT_ID` is set)

## Required Environment Variables / Secrets

The app gracefully degrades when these are missing, but full functionality requires:

- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_KEY` — Supabase API key
- `SECRET_KEY` — Flask session secret key
- `WALLETCONNECT_PROJECT_ID` — WalletConnect project ID
- `CELO_RPC_URL` — Celo RPC endpoint (defaults to `https://forno.celo.org`)
- `GOODDOLLAR_CONTRACT` — GoodDollar token contract address
- `MERCHANT_ADDRESS` — Merchant wallet address for minigames
- `GAMES_KEY` — Private key for games blockchain transactions
- `COMMUNITY_KEY` — Private key for community stories rewards
- `PRODUCTION_DOMAIN` — Production domain (defaults to `https://goodmarket.live`)

## Deployment

Configured for **autoscale** deployment. Run command: `bash -c "node wc_service.js & gunicorn --config gunicorn.conf.py main:app"`
