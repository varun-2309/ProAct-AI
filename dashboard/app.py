import streamlit as st
import requests
import time

# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="ProAct-AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# Custom Dark Theme Styling
# =====================================================
st.markdown("""
<style>
body {
    background-color: #0B0F19;
    color: #E5E7EB;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: #111827;
    padding: 1.5rem;
    border-radius: 14px;
    box-shadow: 0 0 30px rgba(59,130,246,0.08);
}
.badge {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    background-color: #022c22;
    color: #22C55E;
}
.high {
    background-color: #7f1d1d;
    color: #fecaca;
    padding: 1rem;
    border-radius: 12px;
    font-size: 1.2rem;
    font-weight: 700;
}
.low {
    background-color: #022c22;
    color: #bbf7d0;
    padding: 1rem;
    border-radius: 12px;
    font-size: 1.2rem;
    font-weight: 700;
}
.subtitle {
    color: #9CA3AF;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# Hero Section
# =====================================================
st.markdown("## 🧠 ProAct-AI")
st.markdown("### Predict failures before they happen")
st.markdown(
    "<span class='subtitle'>AI-powered predictive maintenance for industrial systems</span>",
    unsafe_allow_html=True
)
st.markdown("<span class='badge'>🟢 Live AI System</span>", unsafe_allow_html=True)
st.markdown("---")

# =====================================================
# Layout
# =====================================================
left, right = st.columns([1, 1.1], gap="large")

# =====================================================
# LEFT: INPUT PANEL
# =====================================================
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔧 Live Sensor Input")

    temperature = st.slider("Temperature (°C)", 40.0, 120.0, 65.0)
    vibration = st.slider("Vibration", 0.1, 2.0, 0.5)
    pressure = st.slider("Pressure", 20.0, 50.0, 30.0)
    rpm = st.slider("RPM", 1000, 2000, 1500)

    payload = {
        "temperature": temperature,
        "vibration": vibration,
        "pressure": pressure,
        "rpm": rpm
    }

    predict = st.button("🔍 Run AI Prediction")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# RIGHT: RESULTS PANEL
# =====================================================
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📊 AI Prediction Results")

    if predict:
        with st.spinner("Running AI inference..."):
            time.sleep(1.2)

            try:
                failure_res = requests.post(
                    "http://127.0.0.1:8000/predict/failure",
                    json=payload
                ).json()

                rul_res = requests.post(
                    "http://127.0.0.1:8000/predict/rul",
                    json=payload
                ).json()

                risk = failure_res["failure_risk"]
                rul = rul_res["estimated_RUL"]

                # Failure Risk
                if risk == "HIGH":
                    st.markdown(
                        "<div class='high'>🔴 HIGH FAILURE RISK<br>Immediate maintenance recommended</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        "<div class='low'>🟢 LOW FAILURE RISK<br>Machine operating normally</div>",
                        unsafe_allow_html=True
                    )

                st.markdown("")

                # RUL
                st.markdown(f"#### ⏳ Remaining Useful Life")
                st.markdown(f"**{rul} cycles**")

                # Health Bar
                health = max(0, min(100, int((rul / 100) * 100)))
                st.progress(health)

                st.caption("Prediction based on live sensor data")

            except Exception:
                st.error("Backend API not reachable. Please ensure FastAPI is running.")

    else:
        st.markdown(
            "<span class='subtitle'>Run a prediction to see AI insights</span>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
