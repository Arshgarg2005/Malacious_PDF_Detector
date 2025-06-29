from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
import tempfile
import os
from flask_cors import CORS

from feature_utils import extract_pdf_features, load_feature_list

app = Flask(__name__)
CORS(app) 
# Load pre-trained components once at startup
model = joblib.load('final_model.pkl')
scaler = joblib.load('scaler.pkl')
#print(type(scaler))
lda = joblib.load('lda.pkl')
feature_list = load_feature_list('features.json')

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        pdf_path = tmp.name

    try:
        features = extract_pdf_features(pdf_path, feature_list)
        print("Features extracted:", features)

        if not features:
            return jsonify({"error": "Failed to extract features from PDF"}), 500

        # Create DataFrame for model input
        df = pd.DataFrame([features], columns=feature_list)
        #print('df',df)
        #feature_cols = df.columns.drop('Class')  # exclude label
        #df_features = df[feature_cols]

# Optional: fill missing values if any
        #df_features = df_features.fillna(0)

        scaled = scaler.transform(df)
        #print("scaled",scaled)

        reduced = lda.transform(scaled)
        #print("red",reduced)
        prediction = model.predict(reduced)[0]
        #print("pred",prediction)
        os.remove(pdf_path)
        return jsonify({"prediction": int(prediction), "label": "Malicious" if prediction == 1 else "Benign"})

    except Exception as e:
        os.remove(pdf_path)
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
