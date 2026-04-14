import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class CryptoSentinelModel:
    def __init__(self, contamination=0.05):
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            n_estimators=200,
            contamination=contamination,
            random_state=42
        )

    def fit(self, df):
        X = self.scaler.fit_transform(df)
        self.model.fit(X)

    def predict(self, df):
        X = self.scaler.transform(df)

        preds = self.model.predict(X)
        scores = self.model.decision_function(X)

        risk = (1 - (scores - scores.min()) /
               (scores.max() - scores.min())) * 100

        result = df.copy()
        result["risk_score"] = risk

        def severity(r):
            if r > 85: return "Critical"
            elif r > 70: return "High"
            elif r > 50: return "Medium"
            else: return "Low"

        result["severity"] = result["risk_score"].apply(severity)
        result["status"] = np.where(preds == -1, "Suspicious", "Normal")

        return result