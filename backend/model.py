import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Load and clean dataset
df = pd.read_csv("PCOS_dataset.csv")

# Clean column names (important to do this first!)
df.columns = df.columns.str.strip()

# Drop irrelevant columns (now these names match correctly)
df.drop(columns=["Sl. No", "Patient File No."], inplace=True)

# Convert specific columns to numeric, handle non-numeric values
df["AMH(ng/mL)"] = pd.to_numeric(df["AMH(ng/mL)"], errors="coerce")
if "II beta-HCG(mIU/mL)" in df.columns:
    df["II beta-HCG(mIU/mL)"] = pd.to_numeric(df["II beta-HCG(mIU/mL)"], errors="coerce")
    df.drop(columns=["II beta-HCG(mIU/mL)"], inplace=True)

# Drop rows with missing values
df.dropna(inplace=True)

# Separate features and target
X = df.drop(columns=["PCOS (Y/N)"])
y = df["PCOS (Y/N)"]

# Encode categorical columns
for col in X.select_dtypes(include=["object"]).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"\n🎯 Model Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(report)


os.makedirs("model", exist_ok=True)

# Save model and feature columns
joblib.dump(model, os.path.join("model", "pcos_model.pkl"))
joblib.dump(X.columns.tolist(), os.path.join("model", "columns.pkl"))


# Function to collect user input
# def get_user_input():
#     data = {
#         "Age (yrs)": int(input("1. What is your age? ")),
#         "Weight (Kg)": float(input("2. What is your weight (in kg)? ")),
#         "Height(Cm)": float(input("3. What is your height (in cm)? ")),
#         "BMI": float(input("4. What is your Body Mass Index (BMI)? (leave blank for auto-calculate) ") or 0),
#         "Waist:Hip Ratio": float(input("5. What is your waist-to-hip ratio? ")),
#         "Cycle(R/I)": 1 if input("6. Is your menstrual cycle regular? (R for Regular / I for Irregular): ").strip().lower() == "r" else 0,
#         "Cycle length(days)": int(input("7. What is your average cycle length (in days)? ")),
#         "Hair growth(Y/N)": 1 if input("9. Hair growth on face/chest? (Yes/No): ").strip().lower() == "yes" else 0,
#         "Weight gain(Y/N)": 1 if input("10. Significant weight gain? (Yes/No): ").strip().lower() == "yes" else 0,
#         "Pimples(Y/N)": 1 if input("11. Frequent acne/pimples? (Yes/No): ").strip().lower() == "yes" else 0,
#         "Hair loss(Y/N)": 1 if input("12. Hair loss/thinning? (Yes/No): ").strip().lower() == "yes" else 0,
#         "Skin darkening (Y/N)": 1 if input("13. Skin darkening (neck/underarms)? (Yes/No): ").strip().lower() == "yes" else 0,
#         "Fast food (Y/N)": 1 if int(input("14. Fast food intake (times per week): ")) > 2 else 0,
#         "Exercise(Y/N)": 1 if input("15. Do you exercise regularly? (Yes/No): ").strip().lower() == "yes" else 0
#     }

#     # Auto-calculate BMI if not provided
#     if data["BMI"] == 0:
#         height_m = data["Height(Cm)"] / 100
#         data["BMI"] = data["Weight (Kg)"] / (height_m ** 2)

#     return pd.DataFrame([data])

# # Get user input and make prediction
# user_input_df = get_user_input()

# # Fill missing columns if any
# missing_cols = set(X.columns) - set(user_input_df.columns)
# for col in missing_cols:
#     user_input_df[col] = 0  # Default value

# # Align columns
# user_input_df = user_input_df[X.columns]

# # Predict
# probability = model.predict_proba(user_input_df)[0][1]
# prediction = model.predict(user_input_df)[0]
# risk_percent = round(probability * 100, 2)

# # Determine risk level
# if risk_percent <= 30:
#     risk_level = "✅ Normal"
# elif risk_percent <= 70:
#     risk_level = "⚠ Moderate Risk"
# else:
#     risk_level = "❗ High Risk"

# # Final report
# print("\n📋 FINAL PCOS RISK REPORT")
# print("-------------------------------")
# print(f"PCOS Risk Probability: {risk_percent}%")
# print(f"Risk Level: {risk_level}")
# print("-------------------------------")

# if prediction == 1:
#     print("🔔 The model predicts you might be at risk of PCOS. Please consult a gynecologist.")
# else:
#     print("👍 The model predicts low risk of PCOS. Maintain a healthy lifestyle.")
