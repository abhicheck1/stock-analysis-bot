Quantitative Market Analysis Pipeline: Nifty 50
Serverless Algorithmic Screening & Data Orchestration
1. Project Overview
This repository contains a production-grade data pipeline designed to automate technical screening for Nifty 50 constituents. The system operates on a serverless architecture, performing daily data ingestion, quantitative transformation, and automated reporting.

Core Objective: To identify high-probability mean-reversion opportunities through rule-based statistical analysis.

2. Technical Architecture
The system follows a modular ETL (Extract, Transform, Load) design pattern, ensuring separation of concerns and system maintainability.

Extraction Layer: Programmatic retrieval of adjusted OHLC (Open, High, Low, Close) data via the yfinance API.

Transformation Layer: Vectorized computation of technical indicators using pandas.

Delivery Layer: Automated distribution of signals via an encrypted SMTP gateway.

3. Quantitative Methodology
The screening logic utilizes a multi-factor authentication model to filter market noise:

A. Trend Analysis (The Filter)
The system employs a Simple Moving Average (SMA) Crossover strategy.

Condition: SMA(20) > SMA(50)

Logic: Ensures the asset is in a medium-term bullish regime before considering an entry.

B. Momentum Modeling (The Trigger)
A 14-day Relative Strength Index (RSI) is used to detect price exhaustion.

Condition: RSI < 45

Logic: Identifies assets that are statistically oversold and prone to a mean-reversion bounce.

4. Technical Stack
5. System Resilience & Error Handling
To ensure "zero-contingency" execution, the pipeline includes:

Exception Wrappers: try-except blocks to prevent pipeline failure during API timeouts or ticker delistings.

Secure Credential Management: Implementation of GitHub Secrets for sensitive environment variables (SENDER_EMAIL, SENDER_PASSWORD).

Stateless Execution: The bot requires no persistent storage, reducing complexity and attack surface.

6. Live Case Study: Infosys (INFY.NS)
Observation Date: February 7, 2026

Technical Profile: * RSI: 18.77 (Extreme Oversold)

CMP: ₹1507.1

Signal Score: 2/2

Inference: The system successfully flagged an extreme liquidity flush-out, identifying a statistically significant entry point for short-term reversal.

7. Developer Intent
This project was architected as a follow-up to the Aspora interview process. It demonstrates:

Technical Agility: Building a live-production tool within 48 hours.

Full-Stack Capability: Managing the lifecycle of data from ingestion to delivery.

Actionable Feedback Loop: Proactively addressing feedback regarding "depth of knowledge" through hands-on engineering.
