# LINKGUARD-AI  
### Explainable AI-Powered URL Phishing & Security Risk Detection System

LINKGUARD-AI is an advanced AI-driven URL security scanner designed to detect phishing and malicious URLs using a hybrid approach that combines machine learning, rule-based security analysis, and explainable AI (XAI). Unlike traditional blacklist-based systems, LINKGUARD-AI analyzes the full URL structure to identify suspicious patterns, brand impersonation, and obfuscation techniques used in modern phishing attacks, including AI-generated threats.

---

## 🚀 Key Features
- Full URL analysis (domain + path + query)
- Phishing and malicious URL detection
- Brand impersonation detection
- Keyword abuse and entropy analysis
- Hybrid ML + rule-based risk fusion
- Explainable AI (SHAP-based explanations)
- Real-time web interface (Flask)
- Risk levels: LOW, MEDIUM, HIGH

---

## 🧠 Technology Stack
- **Backend:** Python, Flask
- **Machine Learning:** Random Forest (Scikit-learn)
- **Explainable AI:** SHAP
- **Frontend:** HTML, CSS, JavaScript
- **Data Processing:** Pandas, NumPy

---

## 📊 Datasets Used
- **PhishTank (verified_online.csv)** – verified phishing URLs  
- **Tranco (tranco_9WJW2.csv)** – legitimate domains  
- **Kaggle Phishing Dataset (phishing_site_urls.csv)**  

---

## ⚙️ How It Works
1. User submits a URL via the web interface
2. Full URL features are extracted (lexical, structural, entropy, brand)
3. Trained ML model predicts phishing probability
4. Hybrid risk fusion adjusts final risk score
5. Explainable AI generates human-readable reasoning
6. Risk level and explanation are displayed to the user

---

## ▶️ How to Run
```bash
pip install -r requirements.txt
cd src
python app.py
