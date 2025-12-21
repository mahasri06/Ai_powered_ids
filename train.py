# train.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

data = pd.read_csv("dataset.csv")

X = data.drop("label", axis=1)
y = data["label"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestClassifier(
    n_estimators=150,
    class_weight="balanced",
    random_state=42
)
model.fit(X_scaled, y)

os.makedirs("model", exist_ok=True)
joblib.dump((model, scaler), "model/ids_model.joblib")

print("✅ Model and scaler trained & saved successfully")
