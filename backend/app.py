from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# Load model and columns
model = joblib.load("model/pcos_model.pkl")
columns = joblib.load("model/columns.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Map inputs
    mapped_data = {
        "Age (yrs)": int(data['age']),
        "Weight (Kg)": float(data['weight']),
        "Height(Cm)": float(data['height']),
        "BMI": float(data['bmi']) if data['bmi'] else 0,
        "Waist:Hip Ratio": float(data['waist_hip_ratio']),
        "Cycle(R/I)": 1 if data['cycle'] == "R" else 0,
        "Cycle length(days)": int(data['cycle_length']),
        "Hair growth(Y/N)": 1 if data['hair_growth'] == "yes" else 0,
        "Weight gain(Y/N)": 1 if data['weight_gain'] == "yes" else 0,
        "Pimples(Y/N)": 1 if data['pimples'] == "yes" else 0,
        "Hair loss(Y/N)": 1 if data['hair_loss'] == "yes" else 0,
        "Skin darkening (Y/N)": 1 if data['skin_darkening'] == "yes" else 0,
        "Fast food (Y/N)": 1 if int(data['fast_food']) > 2 else 0,
        "Exercise(Y/N)": 1 if data['exercise'] == "yes" else 0,
    }

    if mapped_data["BMI"] == 0:
        height_m = mapped_data["Height(Cm)"] / 100
        mapped_data["BMI"] = mapped_data["Weight (Kg)"] / (height_m ** 2)

    input_df = pd.DataFrame([mapped_data])
    for col in columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[columns]

    prob = model.predict_proba(input_df)[0][1]
    prediction = model.predict(input_df)[0]
    risk_percent = round(prob * 100, 2)

    if risk_percent <= 30:
        risk_level = "✅ Normal"
    elif risk_percent <= 70:
        risk_level = "⚠ Moderate Risk"
    else:
        risk_level = "❗ High Risk"

    return jsonify({
        "risk_percent": risk_percent,
        "risk_level": risk_level,
        "prediction": int(prediction),
        "message": "🔔 Consult a gynecologist." if prediction else "👍 Low risk. Maintain a healthy lifestyle."
    })

if __name__ == "__main__":
    app.run(debug=True)
