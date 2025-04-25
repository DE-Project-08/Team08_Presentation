import streamlit as st
import pandas as pd
import boto3
import joblib
import os
import requests
import csv
import io
from datetime import datetime
from transformers import pipeline

# ✅ Set Streamlit page config
st.set_page_config(page_title="Tesla Stock Predictor", layout="centered")

# ✅ Constants and secrets
NEWS_API_KEY = st.secrets["api"]["NEWS_API_KEY"]
BUCKET_NAME = "tesla-stock-sentiment-analysis"
MODEL_FILE = "tesla_model_downloaded.pkl"
PREDICTION_LOG_FILE = "predictions_log.csv"

# ✅ Load model from S3
@st.cache_resource
def load_model():
    s3 = boto3.client("s3")
    s3.download_file(BUCKET_NAME, MODEL_FILE, MODEL_FILE)
    return joblib.load(MODEL_FILE)

model = load_model()

# ✅ Fetch real-time Tesla news sentiment
def fetch_sentiment_score():
    url = f"https://newsapi.org/v2/everything?q=Tesla&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])

    headlines = []
    for art in articles[:5]:
        headlines.append({
            "title": art.get("title", "No Title"),
            "description": art.get("description", "No Description"),
            "publishedAt": art.get("publishedAt", "")[:19].replace("T", " ")
        })

    classifier = pipeline("sentiment-analysis")
    texts = [f"{a['title']}. {a['description']}" for a in headlines]
    sentiments = classifier(texts)
    avg_score = sum(1 if s["label"] == "POSITIVE" else -1 for s in sentiments) / len(sentiments)

    return round(avg_score, 3), headlines

# ✅ Append prediction result to S3 CSV
def upload_prediction_to_s3(data_dict):
    s3 = boto3.client("s3")
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=PREDICTION_LOG_FILE)
        existing_data = obj["Body"].read().decode("utf-8")
        lines = list(csv.reader(io.StringIO(existing_data)))
    except s3.exceptions.NoSuchKey:
        lines = [["Date", "Open", "Close", "Volume", "PriceChange", "SentimentScore", "Prediction"]]

    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [today, data_dict["Open"], data_dict["Close"], data_dict["Volume"],
               data_dict["PriceChange"], data_dict["SentimentScore"], data_dict["Prediction"]]
    lines.append(new_row)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(lines)
    output.seek(0)
    s3.put_object(Bucket=BUCKET_NAME, Key=PREDICTION_LOG_FILE, Body=output.getvalue())

# ✅ Streamlit UI
st.title("📊 Tesla Stock Movement Predictor")
st.markdown("Enter **TODAY'S** stock data to predict **TOMORROW'S** movement.")

open_price = st.number_input("Open Price (Today)", value=0.0)
close_price = st.number_input("Close Price (Today)", value=0.0)
volume = st.number_input("Volume Traded (Today)", value=0)

if st.button("🔍 Predict Tomorrow's Movement"):
    price_change = close_price - open_price
    sentiment_score, news_articles = fetch_sentiment_score()

    input_data = pd.DataFrame([{
        "Open": open_price,
        "Close": close_price,
        "Volume": volume,
        "SentimentScore": sentiment_score,
        "PriceChange": price_change
    }])["Open Close Volume SentimentScore PriceChange".split()]

    prediction = model.predict(input_data)[0]
    direction = "UP" if prediction == 1 else "DOWN"

    if prediction == 1:
        st.success("📈 Tesla stock is predicted to go UP tomorrow 🚀")
    else:
        st.error("📉 Tesla stock is predicted to go DOWN tomorrow 📉")

    # ✅ Export to S3
    upload_prediction_to_s3({
        "Open": open_price,
        "Close": close_price,
        "Volume": volume,
        "PriceChange": price_change,
        "SentimentScore": sentiment_score,
        "Prediction": direction
    })

    # ✅ Show Tesla news
    st.markdown("### 📰 Current Tesla News Headlines")
    for i, a in enumerate(news_articles):
        st.markdown(f"**{i+1}. {a['title']}**")
        st.markdown(f"🕒 *{a['publishedAt']}*")
        st.markdown(f"📝 {a['description'] or 'No Description Available'}")
        st.markdown("---")
