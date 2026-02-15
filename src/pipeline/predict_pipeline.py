import re
import numpy as np
from urllib.parse import urlparse

def get_prediction_features(url):

    features = []

    # 1. Having IP address
    ip_pattern = r'(([0-9]{1,3}\.){3}[0-9]{1,3})'
    features.append(1 if re.search(ip_pattern, url) else 0)

    # 2. URL Length
    features.append(1 if len(url) > 54 else 0)

    # 3. Having @ symbol
    features.append(1 if "@" in url else 0)

    # 4. Prefix-Suffix (- in domain)
    domain = urlparse(url).netloc
    features.append(1 if "-" in domain else 0)

    # 5. Having subdomain
    if domain.count(".") > 2:
        features.append(1)
    else:
        features.append(0)

    # 6. HTTPS
    features.append(0 if url.startswith("https") else 1)

    # Fill remaining features as 0 for now
    while len(features) < 12:
        features.append(0)

    return np.array(features).reshape(1, -1)
