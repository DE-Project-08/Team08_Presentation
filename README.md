# Real-Time Tesla Stock Sentiment Analysis and Prediction Using AWS, Machine Learning, and News Data Integration

## Problem Statement

The challenge is to predict the movement of **Tesla stock prices** based on historical stock data and real-time news sentiment analysis. Financial markets are often influenced by sentiment in the news, making it essential to incorporate both stock price data and news sentiment in predicting future price movements. The goal is to predict whether Tesla’s stock will go **up** or **down** using machine learning.

## Solution

This project leverages **AWS services**, **machine learning**, and **news sentiment analysis** to predict Tesla stock movement:
1. **Stock data** is fetched using **yfinance**.
2. **News data** is fetched from **NewsAPI**.
3. Both datasets are merged, processed, and used to **train a machine learning model**.
4. Predictions are made using the trained model, and the results are presented through a **Streamlit web app**.
5. Visual insights of predictions are displayed using **AWS QuickSight**.

## Data

The project uses two types of data:
1. **Stock Data**: Historical stock data for Tesla, fetched using **yfinance**.
2. **News Data**: Real-time news articles that are analyzed for sentiment using **NewsAPI**.

The merged dataset, which is used for training the machine learning model, is stored in **AWS S3** as **tesla_balanced_training_data.csv**.

## Machine Learning Model

- **AWS SageMaker** is used to **train the machine learning model**. The model predicts whether Tesla's stock will go **up** or **down** based on the input features from stock and news data.
- The trained model, **tesla_model_fixed.pkl**, is saved in **S3** for future use.

## Prediction

- In the **Prediction.ipynb** notebook, the trained model is used to make predictions based on the latest stock data.
- The user can enter the **Open**, **Close**, and **Volume** for today’s Tesla stock data to get predictions for tomorrow’s movement.

## QuickSight Insights

The predictions from the model are automatically saved as **predictions_log.csv** in **S3**. These insights are then visualized using **AWS QuickSight**, where graphs and trends are plotted to show how predictions evolve over time.
