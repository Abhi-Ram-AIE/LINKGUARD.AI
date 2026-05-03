import joblib
import shap
import pandas as pd
import matplotlib.pyplot as plt

from feature_extraction import extract_features

MODEL_PATH = "../models/trained_model.pkl"


def load_model():
    return joblib.load(MODEL_PATH)

def get_shap_values_for_url(url):
    model = load_model()

    features = extract_features(url)
    feature_df = pd.DataFrame([features])

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(feature_df)

    if isinstance(shap_values, list):
        shap_vals = shap_values[1] if len(shap_values) > 1 else shap_values[0]
    else:
        shap_vals = shap_values

    shap_vals = shap_vals[0]

    return list(shap_vals), feature_df.columns.tolist()

def plot_shap_bar(url, save_path="../results/feature_importance.png"):
    """
    Generate and save SHAP feature importance bar plot.
    """
    shap_vals, feature_names = get_shap_values_for_url(url)

    plt.figure(figsize=(9, 5))
    pd.Series(
        shap_vals,
        index=feature_names
    ).sort_values(key=abs).plot(kind="barh")

    plt.title("Explainable AI – Feature Impact on URL Risk", pad=15)
    plt.xlabel("SHAP Value (Impact on Prediction)")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


if __name__ == "__main__":
    test_url = "http://secure-login-paypal.verify-user.info/login"
    plot_shap_bar(test_url)
    print("Explainability generated successfully.")
