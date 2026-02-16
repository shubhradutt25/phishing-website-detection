from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS
import numpy as np
import pandas as pd
from src.pipeline.predict_pipeline import get_prediction_features

app = Flask(__name__)
CORS(app)

model_path = 'artifacts/model.pkl'
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("✅ Backend: Model loaded successfully!")
except Exception as e:
    print(f"❌ Backend: Error loading model at {model_path}: {e}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded on server", "status": "failed"})
    
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "No URL provided", "status": "failed"})

        features = get_prediction_features(url)

        feature_names = [
            "having_IP_Address", "Prefix_Suffix", "having_Sub_Domain", 
            "SSLfinal_State", "Domain_registeration_length", "Request_URL", 
            "URL_of_Anchor", "Links_in_tags", "SFH", "web_traffic", 
            "Google_Index", "Statistical_report"
        ]
        
        features_df = pd.DataFrame(features, columns=feature_names)

        prediction = model.predict(features_df)
        probabilities = model.predict_proba(features_df)
        
        confidence = np.max(probabilities) * 100 
        result = "Phishing" if prediction[0] == 1 else "Safe"

        return jsonify({
            "url": url,
            "prediction": result,
            "confidence": round(confidence, 2),
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"})
    
if __name__ == '__main__':
    print("🚀 Starting Flask server on http://127.0.0.1:5000...")
    app.run(debug=True, port=5000)
