import streamlit as st
import time
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

st.set_page_config(page_title="Google Meet Assistant", layout="wide")
st.title("🌌 Google Meet Assistant")

# ------------------------------
# 🔹 User Input
# ------------------------------
meet_code = st.text_input("Enter Google Meet code (e.g., abc-defg-hij)")

# ------------------------------
# 🔹 Join Meeting
# ------------------------------
if st.button("Join Meeting"):
    if not meet_code:
        st.error("Please enter a meeting code first!")
    else:
        try:
            # ✅ Chromium path (works on Streamlit Cloud)
            chrome_path = "/usr/bin/chromium"
            driver_path = "/usr/bin/chromedriver"

            options = webdriver.ChromeOptions()
            options.binary_location = chrome_path
            options.add_argument("--headless=new")  # run headless on cloud
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--use-fake-ui-for-media-stream")
            options.add_argument("--mute-audio")

            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)

            meet_url = f"https://meet.google.com/{meet_code}"
            st.write(f"🔗 Opening: {meet_url}")
            driver.get(meet_url)

            time.sleep(5)
            st.success("✅ Google Meet opened in Chromium!")

        except Exception as e:
            st.error(f"❌ Failed to open meeting: {e}")

# ------------------------------
# 🔹 OpenAI Setup
# ------------------------------
openai.api_key = "sk-your_api_key_here"  # replace with your key

def ask_ai(question):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"🚨 API Error: {str(e)}"




