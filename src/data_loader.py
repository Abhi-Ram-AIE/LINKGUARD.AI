import pandas as pd
import os

# -----------------------------
# Dataset Directory
# -----------------------------

DATA_DIR = "../datasets"


# -----------------------------
# Dataset Loaders
# -----------------------------

def load_phishtank():
    """
    Load PhishTank dataset (verified phishing URLs).
    """
    path = os.path.join(DATA_DIR, "verified_online.csv")
    df = pd.read_csv(path)
    print("PhishTank Dataset Loaded")
    return df


def load_tranco():
    """
    Load Tranco dataset (legitimate domains).
    """
    path = os.path.join(DATA_DIR, "tranco_9WJW2.csv")
    df = pd.read_csv(path, header=None)
    df.columns = ["rank", "url"]
    print("Tranco Dataset Loaded")
    return df


def load_kaggle():
    """
    Load Kaggle phishing dataset.
    """
    path = os.path.join(DATA_DIR, "phishing_site_urls.csv")
    df = pd.read_csv(path)
    print("Kaggle Dataset Loaded")
    return df
