import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from data_loader import load_phishtank, load_tranco, load_kaggle
from feature_extraction import extract_features


MODEL_PATH = "../models/trained_model.pkl"


def prepare_dataset():
    # Load datasets
    phishtank_df = load_phishtank()
    tranco_df = load_tranco()
    kaggle_df = load_kaggle()

    # --- Normalize column names ---
    phishtank_df = phishtank_df.rename(columns={phishtank_df.columns[1]: "url"})
    tranco_df = tranco_df.rename(columns={tranco_df.columns[1]: "url"})

    # --- Assign labels ---
    phishtank_df["label"] = 1   # Phishing
    tranco_df["label"] = 0      # Legitimate

    kaggle_df["label"] = kaggle_df["label"].map({
        "bad": 1,
        "good": 0
    })

    # Keep only required columns
    phishtank_df = phishtank_df[["url", "label"]]
    tranco_df = tranco_df[["url", "label"]]
    kaggle_df = kaggle_df[["url", "label"]]

    # Combine all datasets
    combined_df = pd.concat(
        [phishtank_df, tranco_df, kaggle_df],
        ignore_index=True
    )

    return combined_df


def train_model():
    df = prepare_dataset()

    # Extract features
    feature_rows = df["url"].apply(extract_features)
    X = pd.DataFrame(list(feature_rows))
    y = df["label"].astype(int)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=25,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)

    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall   :", recall_score(y_test, y_pred))
    print("F1 Score :", f1_score(y_test, y_pred))

    # Save model
    joblib.dump(model, MODEL_PATH)
    print("Model saved to", MODEL_PATH)


if __name__ == "__main__":
    train_model()
