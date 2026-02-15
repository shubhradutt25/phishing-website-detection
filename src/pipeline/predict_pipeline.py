import sys
import pandas as pd
import re
from urllib.parse import urlparse
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = 'artifacts/model.pkl'
            model = load_object(file_path=model_path)
            preds = model.predict(features)
            return preds
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    def __init__(self, url: str):
        self.url = url

    def get_data_as_data_frame(self):
        try:
            parsed_url = urlparse(self.url)
            domain = parsed_url.netloc

            # 1. having_IP_Address (-1 for phishing, 1 for legitimate)
            match_ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain)
            having_ip = -1 if match_ip else 1

            # 2. Prefix_Suffix (-1 if '-' in domain, else 1)
            prefix_suffix = -1 if '-' in domain else 1

            # 3. having_Sub_Domain (>2 dots = phishing, 2 dots = suspicious, 1 dot = legitimate)
            dots = domain.count('.')
            if dots > 2:
                having_sub_domain = -1
            elif dots == 2:
                having_sub_domain = 0
            else:
                having_sub_domain = 1

            # 4. SSLfinal_State (https = 1, http = -1)
            ssl_state = 1 if parsed_url.scheme == 'https' else -1

            # Creating a dictionary of the 12 specific features from the dataset
            # For complex features (like traffic and index), we assign safe defaults 
            # to ensure the prediction runs smoothly without crashing the server.
            custom_data_input_dict = {
                'having_IP_Address': [having_ip],
                'Prefix_Suffix': [prefix_suffix],
                'having_Sub_Domain': [having_sub_domain],
                'SSLfinal_State': [ssl_state],
                'Domain_registeration_length': [1],
                'Request_URL': [1],
                'URL_of_Anchor': [1],
                'Links_in_tags': [1],
                'SFH': [1],
                'web_traffic': [1],
                'Google_Index': [1],
                'Statistical_report': [1]
            }

            return pd.DataFrame(custom_data_input_dict)
        
        except Exception as e:
            raise CustomException(e, sys)
