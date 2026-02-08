import yfinance as yf
import pandas as pd
import numpy as np
import os
import smtplib
from email.message import EmailMessage
from nsepython import nse_eq  # To fetch all NSE symbols

# 1. SETUP & SECRETS
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def get_all_nse_tickers():
    try:
        # Fetching the official equity list from NSE
        df = nse_eq()
        symbols = df['SYMBOL'].tolist()
        return [f"{s}.NS" for s in symbols if isinstance(s, str)]
    except Exception as e:
        print(f"Error fetching NSE list: {e}")
        return ["RELIANCE.NS", "TCS.NS", "INFY.NS"] # Fallback

# 2. THE AI MODEL (Reinforcement Learning Logic)
class StockRLAgent:
    def __init__(self):
        # In a full production app, you would save/load these weights
        self.weights = np.array([0.5, 0.5])  # Initial weights for SMA and RSI
        self.learning_rate = 0.01

    def predict_score(self, features):
        # Simple linear prediction (could be replaced with a Neural Network)
        return np.dot(features, self.weights)

    def update_weights(self, features, reward):
        # Reward/Punish: Adjust weights based on actual price movement
        # If reward is positive (price went up), increase weight for those features
        adjustment = self.learning_rate * reward * features
        self.weights += adjustment

def analyze_all():
    tickers = get_all_nse_tickers()
    agent = StockRLAgent()
    results = []

    print(f"Analyzing {len(tickers)} stocks...")
    
    # Limiting for performance (or use the full list if running on a powerful server)
    for t in tickers[:100]: 
        try:
            data = yf.download(t, period="7mo", interval="1d", progress=False)
            if len(data) < 50: continue
            
            # Technical Indicators
            data['SMA20'] = data['Close'].rolling(window=20).mean()
            data['SMA50'] = data['Close'].rolling(window=50).mean()
            
            # RSI Calculation
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rsi = 100 - (100 / (1 + (gain / loss)))

            curr_price = float(data['Close'].iloc[-1])
            
            # Features for AI Model
            f1 = 1 if data['SMA20'].iloc[-1] > data['SMA50'].iloc[-1] else 0
            f2 = 1 if rsi.iloc[-1] < 45 else 0
            features = np.array([f1, f2])

            # AI Prediction
            ai_score = agent.predict_score(features)
            
            # Reward/Punish Logic (Simulated using previous day's change)
            # In real use, 'reward' is calculated AFTER the next day's market close
            price_change = (data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]
            reward = 1 if price_change > 0 else -1
            agent.update_weights(features, reward)

            results.append({
                "ticker": t, 
                "price": round(curr_price, 2), 
                "ai_score": round(ai_score, 4),
                "trend": "Bullish" if f1 else "Bearish"
            })
        except:
            continue
    
    results.sort(key=lambda x: x['ai_score'], reverse=True)
    return results[:5] # Return Top 5 picks

def send_gmail(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(msg)

# 3. EXECUTION
top_picks = analyze_all()
report_body = "Top AI-Ranked NSE Stocks:\n\n"
for p in top_picks:
    report_body += f"{p['ticker']} | Price: {p['price']} | AI Score: {p['ai_score']} ({p['trend']})\n"

send_gmail("NSE AI Stock Report", report_body)
