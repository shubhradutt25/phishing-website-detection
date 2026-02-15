from flask import Flask, request, jsonify, render_template
import pickle
from flask_cors import CORS
import numpy as np
from src.pipeline.predict_pipeline import get_prediction_features

app = Flask(__name__)

CORS(app)

# Load Model
try:
    with open('artifacts/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

# 🔹 Prediction API
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "No URL provided", "status": "failed"}), 400

        features = get_prediction_features(url)
        prediction = model.predict(features)

        if prediction[0] == 1:
            result = "Phishing"
        else:
            result = "Safe"

        return jsonify({
            "url": url,
            "prediction": result,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"})

if __name__ == '__main__':
    app.run(debug=True)
