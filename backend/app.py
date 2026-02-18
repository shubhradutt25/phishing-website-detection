from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
from flask_cors import CORS


from src.pipeline.predict_pipeline import get_prediction_features

app = Flask(__name__)
CORS(app)


try:
    model = pickle.load(open('artifacts/model.pkl', 'rb'))
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model is not loaded.'}), 500

    try:
        if request.is_json:
            url = request.json.get('url')
        else:
            url = request.form.get('url')

        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        features = get_prediction_features(url)

        feature_names = [
            "having_IP_Address", "Prefix_Suffix", "having_Sub_Domain", 
            "SSLfinal_State", "Domain_registeration_length", "Request_URL", 
            "URL_of_Anchor", "Links_in_tags", "SFH", "web_traffic", 
            "Google_Index", "Statistical_report"
        ]
        data_df = pd.DataFrame(features, columns=feature_names)


        prediction = model.predict(data_df.values)
        probabilities = model.predict_proba(data_df.values)


        confidence = np.max(probabilities) * 100

        output = prediction[0]
        
        if output == 1:
            result = "Safe"
        else:
            result = "Phishing"

        return jsonify({
            'url': url,
            'prediction': result,
            'confidence': round(confidence, 2)
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

