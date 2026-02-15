from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from src.pipeline.predict_pipeline import get_prediction_features

app = Flask(__name__)
CORS(app)

# -----------------------------
# Load Trained Model
# -----------------------------
model = None

try:
    with open('artifacts/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f" Error loading model: {e}")


# -----------------------------
# Health Check Route
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Phishing Detection API is running"})


# -----------------------------
# Prediction API
# -----------------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({
                "error": "Model not loaded",
                "status": "failed"
            }), 500

        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({
                "error": "No URL provided",
                "status": "failed"
            }), 400

        url = data["url"]

        # Feature Extraction
        features = get_prediction_features(url)

        # Model Prediction
        prediction = model.predict(features)

        result = "Phishing" if prediction[0] == 1 else "Safe"

        return jsonify({
            "url": url,
            "prediction": result,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "failed"
        }), 500


# -----------------------------
# Run Server
# -----------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


