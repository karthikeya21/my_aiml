import streamlit as st
import numpy as np
import pickle
import pandas as pd
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# 📌 Load CSV Data
def load_data():
    try:
        data = pd.read_csv('allelopathy.csv', encoding="ISO-8859-1")
        # data.columns = data.columns.str.strip()  
        # data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# 📌 Load Pretrained Models and LabelEncoders
def load_models():
    with open("rf_model.pkl", "rb") as f:
        rf_model = pickle.load(f)
    with open("xgb_model.pkl", "rb") as f:
        xgb_model = pickle.load(f)
    with open("env_model.pkl", "rb") as f:
        env_model = pickle.load(f)
    with open("label_encoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)
    return rf_model, xgb_model, env_model, label_encoders


# 📌 Encode Inputs
def encode_feature(value, mapping):
    return mapping.get(value, -1)


df = load_data()
unique_source_plants = df["Source Plant "].dropna().unique().tolist()
unique_target_plants = df["Target Plants"].dropna().unique().tolist()


def show():
    st.header("Multi-Class Classification Predictor with Environmental Factors")

    rf_model, xgb_model, env_model, label_encoders = load_models()
    
    st.sidebar.header("🔍 Input Features")

    # 📌 User Inputs
    source_plant = st.sidebar.selectbox("Select Source Plant", unique_source_plants)
    target_plant = st.sidebar.selectbox("Select Target Plant", unique_target_plants)
    ph = st.sidebar.slider("Soil pH Level", min_value=3.0, max_value=10.0, step=0.1)
    nitrogen = st.sidebar.selectbox("Nitrogen Level", ["Low", "Moderate", "High"])
    phosphorus = st.sidebar.selectbox("Phosphorus Level", ["Low", "Moderate", "High"])
    potassium = st.sidebar.selectbox("Potassium Level", ["Low", "Moderate", "High"])

    # Encode Source and Target Plants
    if source_plant in label_encoders["Source Plant"].classes_:
      source_encoded = label_encoders["Source Plant"].transform([source_plant])[0]
    else:
      st.error(f"❌ Unknown Source Plant: {source_plant}")
      st.stop()

    if target_plant in label_encoders["Target Plants"].classes_:
      target_encoded = label_encoders["Target Plants"].transform([target_plant])[0]
    else:
      st.error(f"❌ Unknown Target Plant: {target_plant}")
      st.stop()

    # Numeric Encoding for Nitrogen, Phosphorus, and Potassium
    encoded_nitrogen = encode_feature(nitrogen, {"Low": 0, "Moderate": 1, "High": 2})
    encoded_phosphorus = encode_feature(phosphorus, {"Low": 0, "Moderate": 1, "High": 2})
    encoded_potassium = encode_feature(potassium, {"Low": 0, "Moderate": 1, "High": 2})

    # 🚀 Prepare input data (6 Features)
    input_data = np.array([[source_encoded, target_encoded, ph, encoded_nitrogen, encoded_phosphorus, encoded_potassium]])

    # 📌 Function to Predict Environmental Factors
    def infer_environmental_factors(source_plant):
      source_encoded = label_encoders["Source Plant"].transform([source_plant])[0]
      predicted_env = env_model.predict([[source_encoded]])[0]
      return predicted_env

    # 📌 Predict with Selected Model
    model_choice = st.sidebar.radio("Choose Model", ["Random Forest", "XGBoost"])

    if st.button("Predict Effect"):
      if model_choice == "Random Forest":
          prediction = rf_model.predict(input_data)[0]
      elif model_choice == "XGBoost":
          prediction = xgb_model.predict(input_data)[0]

      # 📌 Predict Environmental Factors
      temperature, humidity, density = infer_environmental_factors(source_plant)
      temperature, humidity, density = int(round(temperature)), int(round(humidity)), int(round(density))

      # Reverse Mapping
      effect_mapping_reverse = {
          0: "Strong Inhibition", 1: "Weakened Inhibition",
          2: "No Effect", 3: "Weakened Exhibition", 4: "Strong Exhibition"
      }
      t_mapping_reverse = {0: "10-20°C", 1: "15-25°C", 2: "20-30°C", 3: "25-35°C", 4: "25-30°C"}
      h_mapping_reverse = {0: "Low", 1: "Moderate", 2: "High", 3: "Moderate to Low"}
      d_mapping_reverse = {0: "Low", 1: "Moderate", 2: "High"}

      # 📌 Display Results
      st.success(f"🌿 Predicted Effect: **{effect_mapping_reverse[prediction]}**")
      st.info(f"🌡️ Suggested Temperature: **{t_mapping_reverse[temperature]}**")
      st.info(f"💧 Suggested Humidity: **{h_mapping_reverse[humidity]}**")
      st.info(f"🌱 Suggested Density: **{d_mapping_reverse[density]}**")



