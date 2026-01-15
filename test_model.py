from keras.models import load_model

try:
    model = load_model('emotion_model.h5')
    print("✅ Model loaded successfully.")
    print("🧠 Model summary:")
    model.summary()
except Exception as e:
    print("❌ Error loading model:")
    print(e)
