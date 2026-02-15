from flask import Flask, request, jsonify
import pickle
import numpy as np
# This line connects to the 'Translator' file you just created
from src.pipeline.predict_pipeline import get_prediction_features

app = Flask(__name__)

# 1. Load the Machine Learning Model
try:
    with open('artifacts/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 2. Get the raw URL from the website frontend
        data = request.get_json()
        url = data.get('url') # The frontend should send {"url": "http://..."}

        if not url:
            return jsonify({"error": "No URL provided", "status": "failed"})

        # 3. Use your Pipeline to translate the URL into numbers
        # This uses the 31 features we found in your final_phishing_dataset.csv
        features = get_prediction_features(url)
        
        # 4. Make the prediction
        prediction = model.predict(features)
        
        # 5. Determine the result
        # Most models use 1 for Phishing and -1 or 0 for Safe
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
    # The server will run on http://127.0.0.1:5000
    app.run(debug=True, port=5000)