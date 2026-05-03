def baseline_check(url):
    """
    Simple traditional rule-based detection.
    """

    url_lower = url.lower()

    score = 0

    # Basic checks
    if "https" not in url_lower:
        score += 0.3

    if len(url) > 75:
        score += 0.2

    if any(k in url_lower for k in ["login", "verify", "update"]):
        score += 0.3

    # Risk decision
    if score >= 0.6:
        level = "HIGH"
    elif score >= 0.3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return level