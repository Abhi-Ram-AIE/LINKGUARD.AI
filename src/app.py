from flask import Flask, request, jsonify, render_template

from risk_scoring import assess_url_risk
from explainability import get_shap_values_for_url
from explain_text import generate_explanation
from feature_extraction import extract_features

from threat_classifier import classify_threat
from baseline_model import baseline_check

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check-url", methods=["POST"])
def check_url():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL not provided"}), 400

    url = data["url"]

    try:
        # Features
        features = extract_features(url)

        # Risk scoring
        risk_result = assess_url_risk(url)

        # Explainability
        shap_vals, feature_names = get_shap_values_for_url(url)

        explanation_text = generate_explanation(
            shap_vals,
            feature_names,
            risk_result["risk_level"]
        )

        # Threat classification
        threat_type = classify_threat(features, url)

        # Baseline model
        baseline_result = baseline_check(url)

        return jsonify({
            "url": url,
            "risk_level": risk_result.get("risk_level", "UNKNOWN"),
            "risk_score": int(risk_result.get("risk_score", 0)),
            "malicious_probability": float(risk_result.get("malicious_probability", 0)),
            "explanation": explanation_text,
            "threat_type": threat_type,
            "baseline_result": baseline_result
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)