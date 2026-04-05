# 🎓 GoodMarket — Learn & Earn Feature Guide

> **GoodDollar Ecosystem | Celo Blockchain | April 2026**
> GoodMarket is built by Community Moderators — not an official product of the GoodDollar Foundation.

---

## 📋 Table of Contents

1. [What Changed — Old Feature vs New Feature](#1-what-changed)
2. [How to Take a Quiz](#2-how-to-take-a-quiz)
3. [Achievement Card & NFT Minting](#3-achievement-card--nft-minting)
4. [Mint Eligibility Rules](#4-mint-eligibility-rules)
5. [NFT Marketplace — How to Sell](#5-nft-marketplace--how-to-sell)
6. [How to Burn an NFT](#6-how-to-burn-an-nft)
7. [Transaction History](#7-transaction-history)
8. [Quick Reference Summary](#8-quick-reference-summary)

---

## 1. What Changed

### How the Learn & Earn System Has Changed

GoodMarket Learn & Earn has undergone a major update. Instead of receiving instant G$ rewards after completing a quiz, the new system awards an **Achievement NFT** that can be sold or burned to earn G$ tokens.

### New Earn & Reward Flow

```
Take Quiz  →  Achievement Card  →  Mint as NFT  →  Sell or Burn for G$
```

### Before vs Now

| | ❌ Before (Old Feature) | ✅ Now (New Feature) |
|---|---|---|
| **After Quiz** | Instant G$ reward from smart contract | Achievement Card only |
| **Card Action** | "Sell This Card" button on achievement card | Mint card as NFT on Celo blockchain |
| **Selling** | Card showed "Selling Available on [date]" | List NFT on the marketplace for sale |
| **NFT** | No NFT — only an achievement card | Full NFT on Celo blockchain |
| **Earning G$** | G$ sent directly and immediately to wallet | Sell NFT or burn NFT to receive G$ |
| **Eligibility** | All quizzes eligible | Only quizzes from Feb 11, 2026 onwards |

---

## 2. How to Take a Quiz

### Step-by-Step

1. Connect your GoodDollar wallet by clicking **"Connect GoodDollar Wallet"**
2. Navigate to the **Learn & Earn** page
3. Click the **"Start Quiz"** button to begin
4. Answer each question — you have **20 seconds per question**
5. After all questions are answered, submit your responses
6. Your **Achievement Card** will appear with your score and reward options

> ⚠️ **Important:** You must connect your GoodDollar wallet before starting a quiz. Only **one quiz is allowed every 120 hours (5 days)** per wallet address.

---

## 3. Achievement Card & NFT Minting

### Your Achievement Card

After completing a quiz, your **Achievement Card** appears automatically. This card displays your score and provides actions to mint, download, or share your achievement.

### What the Achievement Card Contains

| Element | Description |
|---|---|
| 🏆 **Score** | Your quiz score (e.g. 9/10 — 90%) |
| 🎨 **Reward** | Achievement NFT — G$ is no longer the direct reward |
| 📅 **Date** | The date and time you completed the quiz |
| 🎨 **Mint as NFT** | Mint your achievement as an NFT on the Celo blockchain |
| 📥 **Download Card** | Save your achievement card as an image file |
| 🐦 **Share** | Share your achievement on Twitter or Telegram |

### How to Mint Your NFT

1. After the quiz, click the **"🎨 Mint as NFT"** button on your Achievement Card
2. Wait for the minting process to complete — **the app pays the gas fee for you**
3. Once done, you will see **"✅ NFT #[number] Minted!"** confirmation
4. Your NFT will now appear in the **"My NFTs"** tab

> 💡 **Gas fees are FREE** — GoodMarket covers all minting costs on your behalf.

---

## 4. Mint Eligibility Rules

### Who Can Mint an NFT?

Not all quizzes are eligible for NFT minting. A cutoff date has been set to protect the integrity of the NFT system.

| Quiz Date | Status | Button Shown |
|---|---|---|
| All of 2025 | 🚫 **NOT ELIGIBLE** | "🚫 Not Eligible (Before Feb 11, 2026)" |
| Jan 1 – Feb 10, 2026 | 🚫 **NOT ELIGIBLE** | "🚫 Not Eligible (Before Feb 11, 2026)" |
| **Feb 11, 2026 and later** | ✅ **ELIGIBLE** | "🎨 Mint as NFT" — active purple button |
| Already minted | ✅ **DONE** | "✅ Already Minted #[token number]" |

### Why Is There a Cutoff Date?

The cutoff date of **February 11, 2026** was set to prevent mass minting from old achievement cards earned before the NFT feature was launched. This ensures marketplace quality and fairness for all users.

### Security Layers

- **Frontend check** — The quiz date is checked instantly on your device; no server call needed for old cards
- **Backend verification** — The server re-verifies the quiz timestamp from the database, even if someone tries to bypass the frontend
- **One quiz = One NFT** — The same quiz cannot be minted twice; duplicate minting is blocked

---

## 5. NFT Marketplace — How to Sell

### Selling Your NFT

After minting an NFT, you can list it for sale in the GoodMarket NFT Marketplace. All transactions are recorded on the Celo blockchain.

#### For the Seller

1. Go to the Learn & Earn page and click the **"My NFTs"** tab
2. Find the NFT you want to sell
3. Click the **"🏷️ List for Sale"** button on the NFT card
4. A modal will appear showing the **suggested price** (based on your quiz score)
5. Confirm the listing — your NFT will appear in the **"NFT Marketplace"** tab
6. When someone buys it, you will receive **G$ tokens** in your wallet

#### For the Buyer

1. Go to the **"🏪 NFT Marketplace"** tab
2. Browse available NFTs — the price in G$ is shown on each card
3. Click the **"💰 Buy NFT"** button on the NFT you want
4. Approve the G$ transfer in your wallet (MetaMask or GoodDollar wallet)
5. Once confirmed, the NFT is transferred to your wallet

### Notes

- The listing price is suggested: **(score / total) × 1,000 G$**
- You can **delist** (remove from sale) your NFT at any time before it is purchased
- All sale transactions are recorded in the **"📜 Tx History"** tab

---

## 6. How to Burn an NFT

### 🔥 NFT Burning — What It Is and How It Works

Burning is the process of **permanently destroying an NFT**. In GoodMarket, when you burn an NFT, you receive a **G$ token reward** calculated from your original quiz score.

### How to Burn an NFT

1. Go to the **"My NFTs"** tab on the Learn & Earn page
2. Find the NFT you want to burn
3. Click the **"🔥 Burn NFT"** button on the NFT card
4. A confirmation modal appears showing your **estimated G$ reward**
5. Confirm the burn — the NFT is sent to the dead address (`0x000...dEaD`)
6. Your **G$ reward** is sent directly to your wallet
7. The burn is recorded in **"📜 Tx History"** → **"🔥 Burn History"** section

### Burn Reward Formula

> **Reward = (score ÷ total questions) × 1,000 G$**

| Quiz Score | Calculation | Burn Reward |
|---|---|---|
| 10/10 — 100% | (10/10) × 1,000 | **1,000 G$** |
| 9/10  — 90% | (9/10) × 1,000 | **900 G$** |
| 8/10  — 80% | (8/10) × 1,000 | **800 G$** |
| 7/10  — 70% | (7/10) × 1,000 | **700 G$** |
| 5/10  — 50% | (5/10) × 1,000 | **500 G$** |

### Important Warnings

- ⚠️ **Burning is permanent** — the NFT cannot be recovered after it is burned
- ⚠️ You cannot burn an NFT that is currently **listed on the marketplace** — delist it first
- ✅ The G$ reward is sent directly to your connected wallet address
- ✅ Every burn transaction has a verifiable link on **CeloScan** blockchain explorer

---

## 7. Transaction History

### 📜 Viewing Your Transaction History

The **"📜 Tx History"** tab displays all your NFT transactions — both sales and burns — in one place.

| Section | Contents | Information Shown |
|---|---|---|
| 💰 **NFT Sales** | All NFTs you have sold | Token #, Quiz name, Price, Seller, Buyer, TX hash, Date |
| 🔥 **Burn History** | All NFTs you have burned | Token #, Quiz, Score, Reward, Wallet, Burn TX, Reward TX, Date |

### How to View Transaction History

1. Connect your wallet on the Learn & Earn page
2. Scroll down to the tab section
3. Click the **"📜 Tx History"** tab
4. The page loads two sections: **"💰 NFT Sales"** and **"🔥 Burn History"**
5. Click any TX hash link to view the transaction on **CeloScan**

> ✅ Every transaction has a link to **CeloScan** (celoscan.io) — the official Celo blockchain explorer — so you can independently verify the authenticity of every sale and burn.

---

## 8. Quick Reference Summary

### All Features at a Glance

| Feature | How to Use | Result |
|---|---|---|
| 🎓 **Take Quiz** | Start Quiz → Answer questions → Submit | Achievement Card + record saved |
| 🎨 **Mint NFT** | Achievement Card → "Mint as NFT" button | NFT minted on Celo (app pays gas) |
| 🏷️ **List for Sale** | My NFTs → "List for Sale" → Set price | NFT appears in marketplace |
| 🛒 **Delist** | My NFTs → "Remove from Sale" | NFT removed from marketplace |
| 💰 **Sell** | Buyer clicks "Buy NFT" → approves G$ → confirms | G$ to seller, NFT to buyer |
| 🔥 **Burn** | My NFTs → "Burn NFT" → Confirm | NFT destroyed, G$ reward received |
| 📜 **History** | "Tx History" tab | All sale and burn records |

### Key Dates & Numbers

| | |
|---|---|
| 📅 **NFT Mint Cutoff** | Quizzes taken before **Feb 11, 2026** are NOT eligible for minting |
| ⏰ **Quiz Cooldown** | 120 hours (5 days) between each quiz attempt |
| 💰 **Maximum Burn Reward** | 1,000 G$ for a perfect score (100%) |
| 🔥 **Burn Reward Formula** | (score ÷ total questions) × 1,000 G$ |
| ⛽ **Gas Fee** | FREE — GoodMarket app pays gas fees for NFT minting |
| 🔗 **Blockchain** | Celo Mainnet — fast and low-cost transactions |
| 🌐 **Block Explorer** | CeloScan (celoscan.io) — verify all transactions |

---

*For questions and support, contact the GoodMarket Community Moderators on Telegram or Twitter/X.*

*GoodMarket is built by Community Moderators — not an official product of the GoodDollar Foundation.*
