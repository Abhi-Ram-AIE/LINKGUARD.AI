import re
import math
from urllib.parse import urlparse, parse_qs

# -----------------------------
# Configuration Lists
# -----------------------------

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "account", "update", "confirm",
    "signin", "bank", "paypal", "amazon", "apple", "google",
    "microsoft", "support", "alert", "security"
]

BRANDS = [
    "paypal", "google", "amazon",
    "apple", "microsoft", "bankofamerica"
]


# -----------------------------
# Helper Functions
# -----------------------------

def shannon_entropy(s):
    if not s:
        return 0
    probs = [float(s.count(c)) / len(s) for c in dict.fromkeys(s)]
    return -sum(p * math.log2(p) for p in probs)


def count_suspicious_keywords(text):
    text = text.lower()
    return sum(1 for word in SUSPICIOUS_KEYWORDS if word in text)


def detect_brand_impersonation(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    for brand in BRANDS:
        if brand in url.lower() and brand not in domain:
            return 1
    return 0


# -----------------------------
# Main Feature Extraction
# -----------------------------

def extract_features(url):
    parsed = urlparse(url)

    domain = parsed.netloc
    path = parsed.path
    query = parsed.query

    tokens = re.split(r"[./\-?_=&]", url)

    features = {}

    # ---------- Basic Lexical ----------
    features["full_url_length"] = len(url)
    features["domain_length"] = len(domain)
    features["path_length"] = len(path)

    features["count_dots"] = url.count(".")
    features["count_hyphens"] = url.count("-")
    features["count_slashes"] = url.count("/")
    features["count_at"] = url.count("@")
    features["count_question"] = url.count("?")
    features["count_equal"] = url.count("=")

    features["digit_count"] = sum(c.isdigit() for c in url)
    features["digit_ratio"] = features["digit_count"] / max(len(url), 1)

    # ---------- Structural ----------
    features["subdomain_depth"] = max(domain.count(".") - 1, 0)
    features["has_ip"] = 1 if re.match(r"\d+\.\d+\.\d+\.\d+", domain) else 0
    features["has_https"] = 1 if parsed.scheme == "https" else 0

    # ---------- Path & Query ----------
    features["query_param_count"] = len(parse_qs(query))
    features["has_login_path"] = 1 if any(
        k in path.lower() for k in ["login", "signin", "verify", "account"]
    ) else 0

    # ---------- Keyword & Brand ----------
    features["suspicious_keyword_count"] = count_suspicious_keywords(url)
    features["brand_impersonation"] = detect_brand_impersonation(url)

    # ---------- Token Analysis ----------
    token_lengths = [len(t) for t in tokens if t]
    features["avg_token_length"] = sum(token_lengths) / max(len(token_lengths), 1)

    # ---------- Entropy & Randomness ----------
    features["url_entropy"] = shannon_entropy(url)
    features["unique_char_ratio"] = len(set(url)) / max(len(url), 1)

    return features
