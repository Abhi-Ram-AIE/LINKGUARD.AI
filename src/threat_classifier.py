def classify_threat(features, url):
    """
    Classify type of threat based on URL behavior.
    """

    url_lower = url.lower()

    # Feature shortcuts
    keywords = features.get("suspicious_keyword_count", 0)
    brand = features.get("brand_impersonation", 0)
    entropy = features.get("url_entropy", 0)
    has_login = "login" in url_lower or "verify" in url_lower

    # Threat rules
    if brand and has_login:
        return "Phishing (Credential Harvesting)"

    if "bank" in url_lower or "paypal" in url_lower:
        return "Financial Fraud Attempt"

    if entropy > 3.5:
        return "Obfuscated / Suspicious URL"

    if keywords >= 3:
        return "Social Engineering Attack"

    return "No Significant Threat"