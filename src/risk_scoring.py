import joblib
import pandas as pd
from urllib.parse import urlparse

from feature_extraction import extract_features

# -----------------------------
# Configuration
# -----------------------------

MODEL_PATH = "../models/trained_model.pkl"

TRUSTED_DOMAINS = {
    "google.com",
    "www.google.com",
    "amazon.com",
    "www.amazon.com",
    "microsoft.com",
    "www.microsoft.com",
    "github.com",
    "www.github.com",
    "wikipedia.org",
    "www.wikipedia.org"
}

# -----------------------------
# Utilities
# -----------------------------

def load_model():
    return joblib.load(MODEL_PATH)


def extract_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return ""


# -----------------------------
# Hybrid Risk Fusion
# -----------------------------

def hybrid_risk_fusion(ml_prob, features):
    """
    Combine ML probability with rule-based security signals.
    """

    brand_score = features.get("brand_impersonation", 0)

    keyword_score = min(
        features.get("suspicious_keyword_count", 0) / 5, 1
    )

    entropy_score = min(
        features.get("url_entropy", 0) / 5, 1
    )

    final_score = (
        0.55 * ml_prob +
        0.20 * brand_score +
        0.15 * keyword_score +
        0.10 * entropy_score
    )

    if final_score >= 0.65:
        risk_level = "HIGH"
    elif final_score >= 0.35:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return final_score, risk_level, brand_score, keyword_score


# -----------------------------
# Final Risk Assessment
# -----------------------------

def assess_url_risk(url):
    """
    Final risk assessment using hybrid fusion
    with trusted-domain intelligence.
    """

    model = load_model()

    # Feature extraction
    features = extract_features(url)
    feature_df = pd.DataFrame([features])

    # ML probability
    ml_prob = model.predict_proba(feature_df)[0][1]

    # Hybrid fusion
    final_score, risk_level, brand_score, keyword_score = hybrid_risk_fusion(
        ml_prob, features
    )

    # Trusted-domain refinement (STEP 1)
    domain = extract_domain(url)

    if (
        domain in TRUSTED_DOMAINS
        and ml_prob < 0.05
        and brand_score == 0
        and keyword_score == 0
        and risk_level != "HIGH"
    ):
        final_score = min(final_score, 0.15)
        risk_level = "LOW"

    return {
    "url": url,
    "malicious_probability": float(round(ml_prob, 4)),
    "risk_score": int(final_score * 100),
    "risk_level": risk_level
    }
