import streamlit as st
import os
from langchain_groq import ChatGroq

# 🔐 API Key (from CMD)
groq_api_key = os.getenv("GROQ_API_KEY")

# 🤖 LLM
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.1-8b-instant",
    groq_api_key=groq_api_key
)

# 🛠️ FUNCTIONS (Terrain Logic)

def calculate_risk(slope, rainfall, soil, elevation):
    score = 0
    reasons = []

    # slope
    if slope >= 35:
        score += 3
        reasons.append("steep slope")
    elif slope >= 20:
        score += 2
        reasons.append("moderate slope")
    else:
        score += 1
        reasons.append("low slope")

    # rainfall
    if rainfall == "heavy":
        score += 3
        reasons.append("heavy rainfall")
    elif rainfall == "moderate":
        score += 2
        reasons.append("moderate rainfall")
    else:
        score += 1
        reasons.append("low rainfall")

    # soil
    if soil in ["loose", "sand", "clay", "wet"]:
        score += 3
        reasons.append(f"{soil} soil")
    else:
        score += 1
        reasons.append(f"{soil} soil")

    # elevation
    if elevation == "high":
        score += 3
        reasons.append("high elevation")
    elif elevation == "medium":
        score += 2
        reasons.append("medium elevation")
    else:
        score += 1
        reasons.append("low elevation")

    # classification
    if score >= 10:
        risk = "❌ High Risk"
    elif score >= 7:
        risk = "⚠️ Medium Risk"
    else:
        risk = "✅ Low Risk"

    return score, risk, reasons


# 🎨 UI
st.set_page_config(page_title="Terrain Risk Analyser", layout="centered")

st.title("⛰️ Terrain Risk Analyser AI")

st.write("Enter terrain details below:")

# Inputs
slope = st.number_input("Slope (degrees)", min_value=0, max_value=90, value=30)

rainfall = st.selectbox("Rainfall", ["low", "moderate", "heavy"])

soil = st.selectbox("Soil Type", ["rocky", "loose", "clay", "sand", "wet"])

elevation = st.selectbox("Elevation", ["low", "medium", "high"])


# Buttons
if st.button("Analyze Terrain"):
    score, risk, reasons = calculate_risk(slope, rainfall, soil, elevation)

    st.success(f"📊 Risk Score: {score}")
    st.warning(f"⚠️ Risk Level: {risk}")
    st.info(f"🧠 Factors: {', '.join(reasons)}")

# -------------------------
# 🤖 AI Chat Section (same as your code)
# -------------------------
st.subheader("💬 Ask AI about terrain")

user_query = st.text_input("Ask anything about terrain risk:")

if st.button("Ask AI"):
    if user_query:
        response = llm.invoke(user_query)
        st.write("🤖 AI:", response.content)