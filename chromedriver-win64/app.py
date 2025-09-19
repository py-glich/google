import streamlit as st
import time
import os
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# ---------------------------
# 🔹 OpenAI API Key
# ---------------------------
openai.api_key = "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"

# ---------------------------
# 🔹 Streamlit UI
# ---------------------------
st.title("Google Meet Assistant 🤖")

meet_code = st.text_input("Enter Google Meet code (e.g., abc-defg-hij)")

if st.button("Join Meeting"):
    try:
        # ---------------------------
        # ✅ Launch Chrome with extension
        # ---------------------------
        service = Service("chromedriver.exe")  # make sure chromedriver.exe is in the same folder
        options = webdriver.ChromeOptions()
        options.add_argument("--use-fake-ui-for-media-stream")  # auto allow mic/cam
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

        # Load your extension (replace path with your extension folder if needed)
        extension_path = os.path.join(os.getcwd(), "extension")  # folder containing your Drive extension
        if os.path.exists(extension_path):
            options.add_argument(f"--load-extension={extension_path}")

        driver = webdriver.Chrome(service=service, options=options)

        # ---------------------------
        # ✅ Open Meet
        # ---------------------------
        meet_url = f"https://meet.google.com/{meet_code}"
        st.write(f"🔗 Opening: {meet_url}")
        driver.get(meet_url)
        time.sleep(10)  # wait for page to load

        st.success("✅ Google Meet opened successfully!")

        # ---------------------------
        # ✅ Subtitle Capture Loop
        # ---------------------------
        subtitle_file = "subtitles.txt"
        response_file = "responses.txt"

        st.write("🎤 Listening for subtitles...")

        subtitle_box = st.empty()
        response_box = st.empty()

        while True:
            try:
                # Example: Extension writes subtitles into subtitles.txt
                if os.path.exists(subtitle_file):
                    with open(subtitle_file, "r", encoding="utf-8") as f:
                        subtitles = f.read().strip()

                    if subtitles:
                        subtitle_box.write(f"**Subtitles:** {subtitles}")

                        # Send to ChatGPT
                        completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a helpful meeting assistant."},
                                {"role": "user", "content": subtitles}
                            ]
                        )

                        reply = completion.choices[0].message["content"].strip()
                        response_box.success(f"💬 ChatGPT: {reply}")

                        # Save response in file
                        with open(response_file, "w", encoding="utf-8") as f:
                            f.write(reply)

                        # clear subtitles after processing
                        with open(subtitle_file, "w", encoding="utf-8") as f:
                            f.write("")

                time.sleep(5)

            except Exception as e:
                st.error(f"⚠️ Error in subtitle loop: {e}")
                break

    except Exception as e:
        st.error(f"❌ Failed to open meeting: {e}")
