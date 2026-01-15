import streamlit as st
from PIL import Image
import datetime
import os
import pandas as pd
from datetime import datetime as dt
from streamlit_autorefresh import st_autorefresh
from fpdf import FPDF
from io import BytesIO
import random
import matplotlib.pyplot as plt
from fpdf.enums import XPos, YPos



FONT_PATH = "D:/Projects/zen_ai_app/fonts/DejaVuSans.ttf"

# Music session state
if "music_on" not in st.session_state:
    st.session_state.music_on = True

if "volume_level" not in st.session_state:
    st.session_state.volume_level = 1.0  # Default full volume


# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Zen-AI: Mindful Productivity",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- STYLES ---
st.markdown("""
<style>
body {
    font-family: 'Noto Serif JP', 'Yu Mincho', serif;
    background-color: #fdfaf6;
    color: #2c2c2c;
}
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.freepik.com/premium-photo/zen-bamboo-fountain-with-water-trickling-bamboo-soothing-beauty-frame-photo-scene-social-post_655090-945879.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    opacity: 0.95;
}
.block-container {
    background-color: rgba(255, 255, 255, 0.85);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}
.breathe-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 30px auto 10px;
}
.circle {
  width: 90px;
  height: 90px;
  background-color: rgba(255, 182, 193, 0.4);
  border-radius: 50%;
  animation: breathe 6s ease-in-out infinite;
}
.breathe-text {
  margin-top: 10px;
  font-size: 1.2em;
  color: #444;
  font-family: 'Yu Mincho', serif;
}
@keyframes breathe {
  0% { transform: scale(1); opacity: 0.6; }
  50% { transform: scale(1.4); opacity: 1; }
  100% { transform: scale(1); opacity: 0.6; }
}
@keyframes fall {
  0%   { transform: translateY(-50px) rotate(0deg); opacity: 0; }
  10%  { opacity: 0.8; }
  100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# --- Auto Refresh ---
st_autorefresh(interval=5000, limit=None, key="emotion_auto")
st_autorefresh(interval=20000, limit=None, key="haiku_refresh")

# --- Language Selection ---
language = st.sidebar.radio("🌐 Choose Language / 言語を選ぶ", ["English", "日本語"])

# --- Zen Quotes ---
quotes = [
    "静寂 — Silence brings clarity",
    "感謝 — Gratitude nourishes the soul",
    "平和 — Peace flows from within",
    "呼吸 — Breath is life",
    "一心 — Single-minded focus",
    "忍耐 — Patience deepens purpose",
    "道 — The way is the goal",
    "禅 — Zen: simplicity, clarity"
]
st.sidebar.markdown("### 🈷️ 今日の禅の言葉")
st.sidebar.markdown(f"**{random.choice(quotes)}**")
st.sidebar.markdown("### 🎴 Zen Calligraphy Quotes / 禅の言葉")
for quote in quotes:
    st.sidebar.markdown(f"- {quote}")

st.sidebar.markdown("---")
st.sidebar.subheader("🎼 Ambient Zen Music")
st.session_state.music_on = st.sidebar.toggle("🔊 Play Music", value=st.session_state.music_on)
st.session_state.volume_level = st.sidebar.slider("🔈 Volume", 0.0, 1.0, st.session_state.volume_level, 0.05)

# --- Title & Clock ---
st.title("🌿 Zen-AI: Mindful Productivity Companion")
now = datetime.datetime.now()
current_time = now.strftime("%A, %d %B %Y • %I:%M %p")
st.markdown(f"#### 🕐 {current_time}")

music_file = "assets/zen_background_music.mp3"
if st.session_state.music_on and os.path.exists(music_file):
    st.audio(music_file, format="audio/mp3", start_time=0)

# --- Emotion Detection (File or Manual Input) ---
valid_emotions = ["Happy", "Sad", "Angry", "Surprise", "Fear", "Disgust", "Neutral"]
default_emotion = "Neutral"

# Try to read from file
detected_emotion = None
if os.path.exists("emotion.txt"):
    try:
        with open("emotion.txt", "r") as f:
            detected = f.read().strip().capitalize()
            if detected in valid_emotions:
                detected_emotion = detected
    except Exception:
        pass

# Sidebar manual override
st.sidebar.markdown("### 🎭 Manual Emotion Input")
manual_emotion = st.sidebar.selectbox("Select your emotion", valid_emotions, index=valid_emotions.index(detected_emotion or default_emotion))

if not detected_emotion:
    st.sidebar.info("Webcam emotion not detected. Using manual input.")


# Use manual if webcam is not running
if detected_emotion and detected_emotion.lower() != "neutral":
    emotion = detected_emotion
elif manual_emotion and manual_emotion.lower() != "neutral":
    emotion = manual_emotion
else:
    emotion = "Neutral"



valid_emotions = ["Happy", "Sad", "Angry", "Surprise", "Fear", "Disgust", "Neutral"]
if emotion not in valid_emotions:
    emotion = "Neutral"

# --- Log Emotion to CSV ---
log_file = "emotion_log.csv"
now_str = dt.now().strftime("%Y-%m-%d %H:%M:%S")

if os.path.exists(log_file):
    df = pd.read_csv(log_file)
else:
    df = pd.DataFrame(columns=["Time", "Emotion"])

if len(df) == 0 or df.iloc[-1]["Emotion"] != emotion:
    new_entry = pd.DataFrame([[now_str, emotion]], columns=["Time", "Emotion"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(log_file, index=False)

# --- Emotion Mappings ---
emotion_action_map = {
    'Happy': {
        "message_en": "You're flowing well! Let’s keep the joy going 🎵",
        "message_ja": "よく流れています！喜びを保ちましょう 🎵",
    },
    'Sad': {
        "message_en": "Take a breath. Here's a peaceful haiku to lift your heart 🌸",
        "message_ja": "深呼吸してください。心を癒す俳句をご覧ください 🌸",
        "haiku": True
    },
    'Angry': {
        "message_en": "Let’s calm the fire within 🔥. Focus on your breath.",
        "message_ja": "心の炎を鎮めましょう 🔥。呼吸に集中してください。",
        "gif": "assets/breathe.gif"
    },
    'Surprise': {
        "message_en": "Take a moment to ground yourself ✍️",
        "message_ja": "少し落ち着きましょう ✍️"
    },
    'Fear': {
        "message_en": "You're stronger than you think 💪",
        "message_ja": "あなたは思っているより強い 💪",
        "quote": "“Fear is only as deep as the mind allows.” — Japanese Proverb"
    },
    'Disgust': {
        "message_en": "Take a short break. Sip some tea 🍵",
        "message_ja": "休憩して、お茶を一口 🍵"
    },
    'Neutral': {
        "message_en": "Enjoy the silence and stillness 🌱",
        "message_ja": "静けさと穏やかさを楽しんでください 🌱"
    }
}

# --- Emotion Labels ---
emotion_labels = {
    "Happy": "Happy 😊" if language == "English" else "嬉しい 😊",
    "Sad": "Sad 😢" if language == "English" else "悲しい 😢",
    "Angry": "Angry 😠" if language == "English" else "怒り 😠",
    "Neutral": "Neutral 😐" if language == "English" else "普通 😐",
    "Fear": "Fear 😨" if language == "English" else "恐れ 😨",
    "Surprise": "Surprise 😲" if language == "English" else "驚き 😲",
    "Disgust": "Disgust 🤢" if language == "English" else "嫌悪 🤢"
}

rec = emotion_action_map.get(emotion, {})
message = rec.get("message_en") if language == "English" else rec.get("message_ja")

# --- Main UI Card ---
st.markdown("""<div style='
    background-color: #ffffffdd;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    position: relative;
    z-index: 10;
'>""", unsafe_allow_html=True)

st.markdown(f"### 🧘 {emotion_labels[emotion]}")
st.markdown(message)

# --- Breathing Animation ---
st.markdown("""
<div class="breathe-container">
  <div class="circle"></div>
  <div class="breathe-text">Breathe In… Breathe Out</div>
</div>
<style>
.breathe-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 30px auto 10px;
}
.circle {
  width: 90px;
  height: 90px;
  background-color: rgba(255, 182, 193, 0.4);
  border-radius: 50%;
  animation: breathe 6s ease-in-out infinite;
}
.breathe-text {
  margin-top: 10px;
  font-size: 1.2em;
  color: #444;
  font-family: 'Yu Mincho', serif;
}
@keyframes breathe {
  0% { transform: scale(1); opacity: 0.6; }
  50% { transform: scale(1.4); opacity: 1; }
  100% { transform: scale(1); opacity: 0.6; }
}
</style>
""", unsafe_allow_html=True)

# --- Emotion Visualization (Bar + Line Chart) ---

st.markdown("### 📊 Recent Emotion Distribution (Last 30 Entries)")

# Bar Chart for recent emotion counts
recent_df = df.tail(30)
emotion_counts = recent_df["Emotion"].value_counts().reindex(valid_emotions, fill_value=0)
st.bar_chart(emotion_counts)

st.markdown("### ⏱️ Emotion Over Time (1-minute intervals)")

# Line Chart grouped by time (1 minute bins)
try:
    df["Time"] = pd.to_datetime(df["Time"])
    df_grouped = df.groupby([pd.Grouper(key="Time", freq="1min"), "Emotion"]).size().unstack().fillna(0)
    st.line_chart(df_grouped)
except Exception as e:
    st.warning(f"Unable to generate line chart: {e}")


# --- Focus Score Metric ---
focus_emotions = ["Happy", "Neutral"]
try:
    total = len(df)
    focused = df["Emotion"].isin(focus_emotions).sum()
    score = round((focused / total) * 100) if total > 0 else 0
    st.metric(label="Mindful Focus Score (%)", value=score)
except Exception:
    st.info("Focus score not available.")

# --- Haiku for Sadness ---
sad_haikus = [
    "Winter solitude—\nIn a world of one color\nThe sound of wind.",
    "Autumn moonlight—\na worm digs silently\ninto the chestnut.",
    "An old silent pond...\nA frog jumps into the pond—\nsplash! Silence again."
]

if emotion == "Sad":
    haiku = random.choice(sad_haikus)
    st.markdown(f"### 🌸 Haiku for Your Heart\n\n{haiku}")

# --- GIF for Angry ---
if emotion == "Angry":
    # Use a URL if you don't have local assets
    gif_url = "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif"
    st.image(gif_url, width=200)

# --- Quote for Fear ---
if emotion == "Fear":
    quote = rec.get("quote")
    if quote:
        st.markdown(f"> {quote}")

# --- Download PDF Report ---

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", FONT_PATH, uni=True)  # Regular
        self.add_font("DejaVu", "B", "D:/Projects/zen_ai_app/fonts/DejaVuSans-Bold.ttf", uni=True)  # Bold

    def header(self):
        self.set_font("DejaVu", "", 14)
        self.cell(0, 10, "Zen-AI Mindful Productivity Report", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def fig_to_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format="PNG", bbox_inches="tight")
    buf.seek(0)
    return buf

def generate_pdf_bytes(emotion_log_df, current_emotion, lang):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("DejaVu", "", 12)

    now_str = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    title = "Zen-AI Mindful Productivity Report" if lang == "English" else "マインドフル生産性レポート"
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)

    current_emo = emotion_labels.get(current_emotion, current_emotion)
    label_current = "Current Emotion" if lang == "English" else "現在の感情"
    label_time = "Generated On" if lang == "English" else "生成日時"

    pdf.cell(200, 10, txt=f"{label_current}: {current_emo}", ln=True)
    pdf.cell(200, 10, txt=f"{label_time}: {now_str}", ln=True)
    pdf.ln(5)

    pdf.set_font("DejaVu", "B", 12)
    history_label = "Recent Emotion History" if lang == "English" else "最近の感情履歴"
    pdf.cell(200, 10, txt=history_label, ln=True)
    pdf.set_font("DejaVu", "", 11)

    for idx, row in emotion_log_df.tail(10).iterrows():
        time_str = row["Time"]
        emo = emotion_labels.get(row["Emotion"], row["Emotion"])
        pdf.cell(200, 8, txt=f"{time_str} — {emo}", ln=True)

        # Add Charts (Bar + Line)
    try:
        # Bar Chart - Emotion Distribution
        emotion_counts = emotion_log_df.tail(30)["Emotion"].value_counts().reindex(valid_emotions, fill_value=0)
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        ax1.bar(emotion_counts.index, emotion_counts.values, color='lightcoral')
        ax1.set_title("Emotion Distribution (Last 30 Entries)")
        bar_img = fig_to_image(fig1)
        plt.close(fig1)

        pdf.image(bar_img, x=10, y=pdf.get_y(), w=180)
        pdf.ln(10)

        # Line Chart - Emotion Timeline
        emotion_log_df["Time"] = pd.to_datetime(emotion_log_df["Time"])
        df_grouped = emotion_log_df.groupby([pd.Grouper(key="Time", freq="1min"), "Emotion"]).size().unstack().fillna(0)
        fig2, ax2 = plt.subplots(figsize=(6, 3))
        df_grouped.plot(ax=ax2, marker='o')
        ax2.set_title("Emotion Over Time")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Count")
        fig2.autofmt_xdate()
        line_img = fig_to_image(fig2)
        plt.close(fig2)

        pdf.image(line_img, x=10, y=pdf.get_y(), w=180)
        pdf.ln(10)

    except Exception as e:
        print("Chart generation failed:", e)



    # Save to BytesIO instead of file
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


if st.button("📥 Download Report / レポートをダウンロード"):
    try:
        pdf_buffer = generate_pdf_bytes(df, emotion, language)
        st.download_button(
            label="📩 Download PDF",
            data=pdf_buffer,
            file_name=f"ZenAI_Report_{dt.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Failed to generate report: {e}")


# --- Sakura Falling Animation ---
# --- Falling Yuna Mankai Gauge Animation ---
st.markdown("""
<style>
.yuna-petal {
  position: fixed;
  top: -50px;
  width: 40px;
  height: 40px;
  background-image: url('https://vignette.wikia.nocookie.net/yuyuyu/images/9/98/Yuna_Mankai_Gauge_5.png/revision/latest?cb=20170719200950');
  background-size: contain;
  background-repeat: no-repeat;
  z-index: 9999;
  pointer-events: none;
  animation-name: fall-yuna;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}
@keyframes fall-yuna {
  0% {
    transform: translateY(-50px) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  100% {
    transform: translateY(120vh) rotate(360deg);
    opacity: 0;
  }
}
</style>
""", unsafe_allow_html=True)

# Generate multiple falling gauge icons
for i in range(12):
    left = random.randint(0, 100)
    duration = random.randint(12, 28)
    delay = random.randint(0, 15)
    st.markdown(f"""
    <div class="yuna-petal" style="
        left: {left}vw;
        animation-duration: {duration}s;
        animation-delay: {delay}s;
    "></div>
    """, unsafe_allow_html=True)


st.markdown("</div>", unsafe_allow_html=True)
