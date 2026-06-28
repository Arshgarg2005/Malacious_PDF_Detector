import io
import json
import os
import sys
from contextlib import redirect_stdout

import joblib
import pandas as pd

from feature_utils import extract_pdf_features, load_feature_list


model = joblib.load('final_model.pkl')
scaler = joblib.load('scaler.pkl')
lda = joblib.load('lda.pkl')
feature_list = load_feature_list('features.json')


def emit(payload, code=0):
    print(json.dumps(payload))
    raise SystemExit(code)


def main():
    if len(sys.argv) < 2:
        emit({'error': 'No file uploaded'}, 1)

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        emit({'error': 'Prediction failed: File not found'}, 1)

    try:
        # Suppress any internal stdout from feature extraction to keep output JSON-only.
        with redirect_stdout(io.StringIO()):
            features = extract_pdf_features(pdf_path, feature_list)

        if not features:
            emit({'error': 'Failed to extract features from PDF'}, 1)

        df = pd.DataFrame([features], columns=feature_list)
        scaled = scaler.transform(df)
        reduced = lda.transform(scaled)
        prediction = model.predict(reduced)[0]

        emit({
            'prediction': int(prediction),
            'label': 'Malicious' if prediction == 1 else 'Benign'
        })
    except Exception as e:
        emit({'error': f'Prediction failed: {str(e)}'}, 1)


if __name__ == '__main__':
    main()
