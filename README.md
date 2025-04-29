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

## Architecture

![image](https://github.com/user-attachments/assets/2e9702b9-0193-4910-81e0-09423696c88a)

## QuickSight Insights

The predictions from the model are automatically saved as **predictions_log.csv** in **S3**. These insights are then visualized using **AWS QuickSight**, where graphs and trends are plotted to show how predictions evolve over time.

![Screenshot 2025-04-27 165342](https://github.com/user-attachments/assets/2ae42441-666f-408f-b59b-8eb932ecfc27)

![Screenshot 2025-04-27 163137](https://github.com/user-attachments/assets/42944110-2732-41b3-a8b7-290201eaadf9)

![Screenshot 2025-04-27 171210](https://github.com/user-attachments/assets/ed38cdab-459f-407d-8c65-e7dc04c16d3c)

## StreamLit

![Screenshot 2025-04-28 002013](https://github.com/user-attachments/assets/71d61b35-57f6-4223-81a5-8ef5e172cc22)

![Screenshot 2025-04-28 002028](https://github.com/user-attachments/assets/de145d20-d9d1-4041-9abf-049276c1b3ff)
