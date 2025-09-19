import streamlit as st
import os
import time
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ✅ Your OpenAI API Key
openai.api_key = "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"

# ✅ Path to chromedriver.exe (same folder as app.py)
DRIVER_PATH = os.path.join(os.path.dirname(__file__), "chromedriver.exe")

# --------------------------
# 🔹 Function to join Google Meet
# --------------------------
def open_meet(meet_code):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # ✅ Use local chromedriver.exe
        service = Service(DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(f"https://meet.google.com/{meet_code}")
        return driver
    except Exception as e:
        st.error(f"❌ Failed to open meeting: {e}")
        return None

# --------------------------
# 🔹 Streamlit UI
# --------------------------
st.set_page_config(page_title="Google Meet Assistant", layout="centered")

st.title("🤖 Google Meet Assistant")

meet_code = st.text_input("Enter Google Meet code (e.g., abc-defg-hij):")

if st.button("Join Meeting"):
    if meet_code.strip():
        driver = open_meet(meet_code.strip())
        if driver:
            st.success("✅ Google Meet opened successfully!")
        else:
            st.error("⚠️ Could not join the meeting.")
    else:
        st.warning("Please enter a valid Google Meet code.")






