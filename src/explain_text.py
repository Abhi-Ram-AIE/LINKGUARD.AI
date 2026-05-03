import numpy as np

FEATURE_EXPLANATIONS = {
    "brand_impersonation": "the URL impersonates a well-known brand",
    "suspicious_keyword_count": "the URL contains suspicious keywords",
    "has_login_path": "the URL contains a login or verification path",
    "url_entropy": "the URL appears random or obfuscated",
    "digit_ratio": "the URL contains many digits",
    "subdomain_depth": "the URL uses excessive subdomains",
}


def generate_explanation(shap_values, feature_names, risk_level, top_k=3):
    shap_values = np.array(shap_values).flatten()

    feature_impact = list(zip(feature_names, shap_values))
    feature_impact.sort(key=lambda x: abs(x[1]), reverse=True)

    reasons = []

    for feature, value in feature_impact[:top_k]:
        if value > 0 and feature in FEATURE_EXPLANATIONS:
            reasons.append(FEATURE_EXPLANATIONS[feature])

    # ✅ Context-aware explanation
    if risk_level == "LOW":
        return "The URL appears safe with no strong indicators of phishing."

    if risk_level == "MEDIUM":
        if reasons:
            return "The URL shows some suspicious patterns: " + ", ".join(reasons) + "."
        return "The URL has minor anomalies but no strong threat indicators."

    if risk_level == "HIGH":
        if reasons:
            return "The URL is risky because " + ", ".join(reasons) + "."
        return "The URL exhibits strong phishing characteristics."

    return "No analysis available."