import yfinance as yf
import pandas as pd
import smtplib
import os
from email.message import EmailMessage

# Fetching secrets from GitHub environment
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

TICKERS = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "HINDUNILVR.NS", "ITC.NS", "SBI.NS"]

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

def analyze():
    results = []
    for t in TICKERS:
        try:
            data = yf.download(t, period="7mo", interval="1d", progress=False)
            data['SMA20'] = data['Close'].rolling(window=20).mean()
            data['SMA50'] = data['Close'].rolling(window=50).mean()
            
            # Simple RSI
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))

            curr_price = float(data['Close'].iloc[-1])
            last_rsi = float(rsi.iloc[-1])
            
            score = 0
            if data['SMA20'].iloc[-1] > data['SMA50'].iloc[-1]: score += 1
            if last_rsi < 45: score += 1
            
            results.append({"ticker": t, "price": round(curr_price, 2), "rsi": round(last_rsi, 2), "score": score})
        except: continue
    
    results.sort(key=lambda x: x['score'], reverse=True)
    best = results[0]
    return f"Best Stock: {best['ticker']}\nPrice: {best['price']}\nRSI: {best['rsi']}\nScore: {best['score']}/2"

report = analyze()
send_gmail("Daily Stock Pick", report)
