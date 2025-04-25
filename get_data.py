# ==================================================
# 📊 Tesla Combined News + Stock Data Pipeline
# ==================================================

from newsapi import NewsApiClient
from textblob import TextBlob
import pandas as pd
import yfinance as yf
from datetime import datetime

# -------------------------
# CONFIGURATION
# -------------------------
news_api_key = 'fed8d7fc5e6b4a5a9b96fb4c3938b509'

# -------------------------
# STEP 1: FETCH NEWS & SENTIMENT
# -------------------------
print("📥 Fetching Tesla news...")

newsapi = NewsApiClient(api_key=news_api_key)
news = newsapi.get_everything(q='Tesla', language='en', sort_by='publishedAt', page_size=50)

news_data = []
for article in news['articles']:
    published = article.get('publishedAt', '')
    date_only = published[:10] if published else ''
    title = article.get('title', '')
    desc = article.get('description', '')
    content = f"{title} {desc}"
    score = TextBlob(content).sentiment.polarity
    news_data.append([date_only, title, score])

df_news = pd.DataFrame(news_data, columns=['Date', 'Title', 'SentimentScore'])

# Clean and group by Date
df_news['SentimentScore'] = pd.to_numeric(df_news['SentimentScore'], errors='coerce')
df_news = df_news[df_news['SentimentScore'].notna()]
df_avg_sentiment = df_news.groupby('Date').agg({'SentimentScore': 'mean'}).reset_index()

# -------------------------
# STEP 2: FETCH TESLA STOCK DATA
# -------------------------
print("📈 Fetching Tesla stock price...")

tsla_data = yf.download("TSLA", period="30d", interval="1d", auto_adjust=False)
tsla_data.reset_index(inplace=True)

# Normalize stock date format to 'YYYY-MM-DD'
tsla_data['Date'] = pd.to_datetime(tsla_data['Date']).dt.strftime('%Y-%m-%d')

df_stock = tsla_data[['Date', 'Open', 'Close', 'Volume']]

# -------------------------
# STEP 3: MERGE BOTH DATASETS ON 'Date'
# -------------------------
print("🔗 Merging news sentiment with stock data...")

df_avg_sentiment['Date'] = df_avg_sentiment['Date'].astype(str)
df_combined = pd.merge(df_stock, df_avg_sentiment, on='Date', how='inner')

# -------------------------
# STEP 4: SAVE FINAL COMBINED CSV
# -------------------------
output_file = "combined_tesla_data.csv"
df_combined.to_csv(output_file, index=False)
print(f"✅ Combined file saved as: {output_file}")

# Show preview
print("\n📄 Sample Output:")
print(df_combined.head())
