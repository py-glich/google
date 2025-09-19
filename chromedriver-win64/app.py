import streamlit as st
import time
import openai
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By

# ✅ Auto install ChromeDriver
chromedriver_autoinstaller.install()

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
            # ✅ Chrome options
            options = webdriver.ChromeOptions()
            options.add_argument("--use-fake-ui-for-media-stream")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--mute-audio")

            # ✅ Launch Chrome
            driver = webdriver.Chrome(options=options)

            meet_url = f"https://meet.google.com/{meet_code}"
            st.write(f"🔗 Opening: {meet_url}")
            driver.get(meet_url)

            time.sleep(5)
            st.success("✅ Chrome opened Google Meet!")

        except Exception as e:
            st.error(f"❌ Failed to open meeting: {e}")

# ------------------------------
# 🔹 OpenAI Setup
# ------------------------------
openai.api_key = "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"  # replace with your key

def ask_ai(question):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"🚨 API Error: {str(e)}"


