# 📊 SaleSight – ML Pipeline Integration

## Overview

This project implements an end-to-end data science pipeline for sales prediction using machine learning models integrated into a production-ready architecture.

The system connects:

- Data Sources (ERP, CRM, CSV, APIs, Web Scraping)
- ETL / Data Pipeline
- Feature Engineering Layer
- Machine Learning Models
- Model Serving API
- Visualization Dashboard (Power BI / Web App)

The system allows users to:

1. Ingest historical sales data  
2. Transform and validate datasets  
3. Train and evaluate predictive models  
4. Generate sales forecasts  
5. Monitor model performance  

---

## 🔌 Data Pipeline Architecture

### Data Sources

- ERP system (sales transactions)
- CRM (customer data)
- Marketing platforms
- External economic indicators
- Web scraped competitor data (optional)

### ETL Framework

- Extraction: Automated batch ingestion
- Transformation: Cleaning, encoding, feature generation
- Load: Data Warehouse / Data Lake

### Storage

- Raw Layer (unprocessed data)
- Processed Layer (cleaned and validated)
- Feature Store (model-ready dataset)

---

## 🧠 Model Behavior

The prediction system must:

- Validate input schema before inference
- Handle missing values automatically
- Detect outliers
- Support:
  - Daily forecasts
  - Weekly forecasts
  - Monthly forecasts
- Return structured prediction outputs
- Log predictions for monitoring

---

## 📊 Feature Engineering Strategy

### Core Feature Groups

#### 1️⃣ Temporal Features  
- Day of week  
- Month  
- Seasonality  
- Holidays  

#### 2️⃣ Commercial Features  
- Promotions  
- Discounts  
- Marketing campaigns  

#### 3️⃣ Customer Features  
- Segment  
- Purchase frequency  
- Average ticket  

#### 4️⃣ External Features  
- Inflation rate  
- Exchange rate  
- Competitor price index  

---

## 🤖 Machine Learning Models

### Baseline Models
- Linear Regression
- Ridge
- Lasso

### Tree-Based Models
- Random Forest
- Gradient Boosting (XGBoost / LightGBM)

### Time Series Models
- ARIMA
- Prophet
- LSTM (if deep learning is required)

---

## 📈 Model Evaluation

The system must compute:

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
- R² Score

### Validation Strategy

- Time Series Split
- Backtesting validation
- Rolling window evaluation

---

## 🚀 Model Deployment

### Serving Layer

- REST API (FastAPI)
- Batch prediction endpoint
- Real-time prediction endpoint

### Example Prediction Request

```json
{
  "date": "2026-03-01",
  "store_id": 12,
  "product_id": 450,
  "promotion": 1,
  "price": 19.99
}