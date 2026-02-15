import numpy as np

def get_prediction_features(url):
    # This creates a list of 31 numbers for the model
    # Based on the 'final_phishing_dataset.csv' you provided
    features = [0] * 31 
    
    # Simple logic to show it's working:
    if len(url) > 50: features[2] = 1  # URL Length
    if "@" in url: features[4] = 1     # At Symbol
    if "https" not in url: features[8] = -1 # SSL State
    
    return np.array(features).reshape(1, -1)