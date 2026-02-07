Quantitative Market Analysis Pipeline: Nifty 50
A Serverless, End-to-End Algorithmic Screening System

Project Overview
This repository contains a production-ready data pipeline designed to automate the technical analysis of Nifty 50 constituents. The system operates on a serverless architecture to ingest market data, calculate statistical indicators, and distribute actionable signals through a secure notification gateway.

The primary objective of this project is to demonstrate competency in data engineering, algorithmic logic, and automated cloud orchestration.

Technical Architecture
The system is structured as a modular ETL (Extract, Transform, Load) pipeline:

Data Ingestion (Extract): Leverages the yfinance API to retrieve historical adjusted closing prices. The system is designed to handle market volatility and data gaps by implementing robust error-handling protocols.

Quantitative Transformation (Transform): * Trend Analysis: Utilizes Simple Moving Average (SMA) crossovers (20-day vs. 50-day) to filter for assets in a bullish regime.

Momentum Modeling: Implements a 14-day Relative Strength Index (RSI) calculation to detect mean-reversion opportunities.

Notification Layer (Load): Utilizes the SMTP protocol to transmit findings via an encrypted channel, ensuring stakeholders receive analysis prior to market opening.

Technical Stack
Programming Language: Python 3.9+

Data Analysis: Pandas (Vectorized data processing), NumPy

Orchestration: GitHub Actions (YAML-based CI/CD)

Data Source: Yahoo Finance API

Communication: SMTP via Google Secure App Gateway

Algorithmic Methodology
The screening logic is based on a dual-factor authentication model:

Trend Confirmation: The asset must maintain a short-term SMA (20) above the long-term SMA (50), ensuring that mean-reversion attempts are aligned with broader market strength.

Statistical Exhaustion: The system flags assets with an RSI below 45. Extreme cases (e.g., RSI < 20) are prioritized as high-probability reversal candidates.

Resiliency: The script incorporates comprehensive exception handling to manage API timeouts, ticker delistings, or zero-division errors during volatility calculations.

Performance Case Study: INFOSYS (INFY.NS)
Signal Date: February 7, 2026

Analysis: The pipeline identified a significant price-momentum divergence in INFY.NS.

Metrics: RSI 18.77 | CMP 1507.1

Inference: The data indicated an extreme oversold condition, marking a statistically significant entry point for short-term mean reversion.

Developer Intent
This project was initiated as a direct response to technical feedback during the Aspora interview process. It serves to validate:

Technical Agility: The ability to architect and deploy a functional financial tool within a 48-hour window.

Systems Thinking: Understanding how to integrate disparate services (API, Python, GitHub Cloud, SMTP) into a single, zero-maintenance product.

Domain Depth: Moving beyond surface-level charting into programmed, rule-based quantitative analysis.

Implementation Instructions
Environment Variables: Ensure SENDER_EMAIL, SENDER_PASSWORD, and RECEIVER_EMAIL are configured in the repository secrets.

Schedule: The main.yml workflow is set to trigger at 03:30 UTC (09:00 IST) every Monday through Friday.

Manual Override: The pipeline supports workflow_dispatch for on-demand analysis.
