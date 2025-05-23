# Streamlit Web App for Deficiency Risk Prediction
import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

# Define the prediction model class
class DeficiencyRiskModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = LogisticRegression(max_iter=1000)
        self.columns = [
            'sleeptimecheckresult',
            'vitmaindcheckresult',
            'budget_10萬 ~ 20萬',
            'budget_20萬 ~ 30萬',
            'budget_30萬以上',
            'budget_5萬 ~ 10萬',
            'budget_5萬以下'
        ]

    def fit(self, df):
        df = df.copy()
        df = df.dropna(subset=["sleeptimecheckresult", "vitmaindcheckresult", "budget"])
        X = pd.get_dummies(df[["sleeptimecheckresult", "vitmaindcheckresult", "budget"]], drop_first=True)
        y = ((df["sleeptimecheckresult"] < 8) & (df["vitmaindcheckresult"] < 20)).astype(int)
        self.columns = X.columns
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict_proba(self, sleep, vitamin_d, budget):
        data = pd.DataFrame({
            'sleeptimecheckresult': [sleep],
            'vitmaindcheckresult': [vitamin_d],
            'budget': [budget]
        })
        X = pd.get_dummies(data, drop_first=True)
        for col in self.columns:
            if col not in X.columns:
                X[col] = 0
        X = X[self.columns]
        X_scaled = self.scaler.transform(X)
        prob = self.model.predict_proba(X_scaled)[0, 1]
        return prob

# Load sample data for training (you will replace this with real dataset)
df_placeholder = pd.DataFrame({
    'sleeptimecheckresult': np.random.uniform(5, 9, 200),
    'vitmaindcheckresult': np.random.uniform(10, 40, 200),
    'budget': np.random.choice([
        '5萬以下', '5萬 ~ 10萬', '10萬 ~ 20萬',
        '20萬 ~ 30萬', '30萬以上'
    ], 200)
})

# Fit model
model = DeficiencyRiskModel()
model.fit(df_placeholder)

# Streamlit app interface
st.title("Deficiency Risk Prediction Tool")

sleep = st.slider("Sleep Duration (hours)", 4.0, 10.0, 7.0, 0.5)
vit_d = st.slider("Vitamin D Level (ng/mL)", 5.0, 50.0, 25.0, 0.5)
budget = st.selectbox("Monthly Budget Range", [
    '5萬以下', '5萬 ~ 10萬', '10萬 ~ 20萬', '20萬 ~ 30萬', '30萬以上'
])

if st.button("Predict Risk"):
    risk = model.predict_proba(sleep, vit_d, budget)
    st.success(f"Predicted deficiency risk: {risk:.2%}")
