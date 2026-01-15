# ui/suggestions_panel.py
import streamlit as st
from suggestion_engine import get_suggestions

def render_suggestions_panel(emotion):
    if not emotion:
        st.info("No emotion detected yet.")
        return

    data = get_suggestions(emotion)
    suggestions = data["suggestions"]
    quote = data["quote"]

    with st.container():
        st.markdown("""
        <style>
            .suggestion-box {
                background-color: #f9f9f9;
                padding: 1.2rem;
                border-radius: 15px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                margin-top: 20px;
                font-family: 'Noto Sans JP', sans-serif;
            }
            .suggestion-title {
                font-size: 1.4rem;
                font-weight: 600;
                color: #333;
            }
            .quote {
                font-style: italic;
                color: #666;
                margin-bottom: 1rem;
            }
            .tip {
                font-size: 1rem;
                margin: 0.2rem 0;
                color: #444;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="suggestion-box">
            <div class="suggestion-title">🧠 Mood-Based Suggestions</div>
            <div class="quote">“{quote}”</div>
            <div class="tip">💡 {suggestions[0]}</div>
            <div class="tip">💡 {suggestions[1]}</div>
        </div>
        """, unsafe_allow_html=True)
