import re
import numpy as np
import whois
import requests
import tldextract
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime

def get_prediction_features(url):
    features = []
    
    if not re.match(r"^https?", url):
        url = "http://" + url

    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        extracted = tldextract.extract(url)
        main_domain = f"{extracted.domain}.{extracted.suffix}"
        
        # Fetch Website Content
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            site_accessible = True
        except:
            soup = None
            site_accessible = False

        # --- 1. having_IP_Address ---
        # If IP is used -> Phishing (-1), else Safe (1)
        ip_pattern = r'(([0-9]{1,3}\.){3}[0-9]{1,3})'
        features.append(-1 if re.search(ip_pattern, url) else 1)

        # --- 2. Prefix_Suffix ---
        # If domain has "-" -> Phishing (-1), else Safe (1)
        features.append(-1 if "-" in domain else 1)

        # --- 3. having_Sub_Domain ---
        # 1 dot = Safe (1), 2 dots = Suspicious (0), >2 dots = Phishing (-1)
        clean_domain = domain.replace("www.", "")
        dot_count = clean_domain.count(".")
        if dot_count == 1:
            features.append(1) # Safe
        elif dot_count == 2:
            features.append(0) # Suspicious
        else:
            features.append(-1) # Phishing

        # --- 4. SSLfinal_State ---
        # HTTPS -> Safe (1), HTTP -> Phishing (-1)
        # (Real datasets check certificate age/issuer, but this is a good proxy)
        if parsed_url.scheme == "https":
            features.append(1)
        else:
            features.append(-1)

        # --- 5. Domain_registeration_length ---
        # Expiring < 1 year -> Phishing (-1), else Safe (1)
        try:
            w = whois.whois(domain)
            exp_date = w.expiration_date
            if isinstance(exp_date, list):
                exp_date = exp_date[0]
            
            if exp_date:
                days_left = (exp_date - datetime.now()).days
                features.append(-1 if days_left < 365 else 1)
            else:
                features.append(-1) # Cannot verify -> Risky
        except:
            features.append(-1) # Error -> Risky

        # --- 6. Request_URL ---
        # High % of external objects -> Phishing (-1), else Safe (1)
        if soup:
            i = 0
            success = 0
            for tag in soup.find_all(['img', 'audio', 'embed', 'iframe']):
                src = tag.get('src')
                if src:
                    i += 1
                    if main_domain in src or src.startswith(('/', '#')):
                        success += 1
            
            if i > 0:
                percentage = (success / i) * 100
                features.append(1 if percentage >= 22 else -1) # < 22% internal is bad
            else:
                features.append(1) # No objects -> Assume Safe
        else:
            features.append(-1) # Site down

        # --- 7. URL_of_Anchor ---
        # High % of external anchors -> Phishing (-1)
        if soup:
            i = 0
            unsafe = 0
            for a in soup.find_all('a', href=True):
                href = a['href']
                if "#" in href or "javascript" in href.lower() or "mailto" in href:
                    unsafe += 1
                elif not (main_domain in href or href.startswith('/')):
                    unsafe += 1
                i += 1

            if i > 0:
                percentage = (unsafe / i) * 100
                if percentage < 31:
                    features.append(1) # Safe
                elif 31 <= percentage <= 67:
                    features.append(0) # Suspicious
                else:
                    features.append(-1) # Phishing
            else:
                features.append(1)
        else:
            features.append(-1)

        # --- 8. Links_in_tags ---
        # High % of external meta/script links -> Phishing (-1)
        if soup:
            i = 0
            success = 0
            for tag in soup.find_all(['meta', 'script', 'link']):
                link = tag.get('href') or tag.get('src')
                if link:
                    i += 1
                    if main_domain in link or link.startswith(('/', '#')):
                        success += 1
            
            if i > 0:
                percentage = (success / i) * 100
                if percentage < 17:
                    features.append(-1) # Phishing
                elif 17 <= percentage <= 81:
                    features.append(0) # Suspicious
                else:
                    features.append(1) # Safe
            else:
                features.append(1)
        else:
            features.append(-1)

        # --- 9. SFH (Server Form Handler) ---
        # Empty action -> Phishing (-1)
        if soup:
            forms = soup.find_all('form', action=True)
            if len(forms) > 0:
                risk = 1 # Assume safe initially
                for form in forms:
                    action = form['action']
                    if action == "" or action == "about:blank":
                        risk = -1 # Phishing
                    elif main_domain not in action and not action.startswith('/'):
                        risk = 0 # Suspicious (sending data elsewhere)
                features.append(risk)
            else:
                features.append(1) # No forms -> Safe
        else:
            features.append(-1)

        # --- 10. web_traffic ---
        # Rank < 100,000 -> Safe (1), > 100,000 -> Suspicious (0), Not found -> Phishing (-1)
        # Without API, we assume: Accessible = 1, Not Accessible = -1
        features.append(1 if site_accessible else -1)

        # --- 11. Google_Index ---
        # Indexed -> 1, Not -> -1
        features.append(1 if site_accessible else -1)

        # --- 12. Statistical_report ---
        # Clean -> 1, Phishing List -> -1
        features.append(1) # Assume clean to prevent false positives

        print(f"DEBUG FEATURES: {features}")
        return np.array(features).reshape(1, -1)

    except Exception as e:
        print(f"Extraction Error: {e}")
        # Return a safe default array (1s) to prevent crashing
        return np.array([1] * 12).reshape(1, -1)
