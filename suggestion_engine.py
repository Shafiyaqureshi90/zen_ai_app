# suggestion_engine.py
import random
import json

SUGGESTIONS = {
    "happy": ["Keep going! You're doing great!", "Take a short break to enjoy this moment."],
    "sad": ["Try a 5-min breathing exercise.", "Step outside and get some fresh air."],
    "angry": ["Deep breaths. Maybe a walk will help.", "Write down what's frustrating you."],
    "neutral": ["Maintain your focus. Stay consistent.", "Time for a quick Pomodoro?"],
    "surprised": ["Take a moment to reflect.", "Channel this into creativity!"],
    "disgust": ["Time to reset with a deep breath.", "Clean your space — it might help."],
    "fear": ["You're safe. Try grounding techniques.", "Slow breathing can calm your nerves."]
}

def load_quotes(path="assets/quotes.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_suggestions(emotion):
    base = SUGGESTIONS.get(emotion, ["Stay mindful."])
    quote = random.choice(load_quotes())
    return {
        "suggestions": base,
        "quote": quote
    }
