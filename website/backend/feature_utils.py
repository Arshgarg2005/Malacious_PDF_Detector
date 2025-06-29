import json
from PyPDF2 import PdfReader

def load_feature_list(feature_file='features.json'):
    with open(feature_file, 'r') as f:
        return json.load(f)

def extract_pdf_features(pdf_path, feature_list=None):
    features = {}

    try:
        with open(pdf_path, 'rb') as f:
            data = f.read()
            size = len(data)
            data_str = data.decode('latin1', errors='ignore')
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return {}

    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata or {}
        num_pages = len(reader.pages)
        is_encrypted = int(reader.is_encrypted)
    except Exception as e:
        print(f"Error parsing PDF structure: {e}")
        metadata = {}
        num_pages = 0
        is_encrypted = 0

    features['pdfsize'] = size
    features['metadata size'] = len(str(metadata))
    features['pages'] = num_pages
    features['xref Length'] = data_str.count('xref')
    features['title characters'] = len(metadata.get('/Title', ''))
    features['isEncrypted'] = is_encrypted
    features['embedded files'] = data_str.count('/EmbeddedFile')
    features['images'] = data_str.count('/Image')
    features['text'] = int('/Font' in data_str or '/Text' in data_str)
    features['header'] = int(data_str.startswith('%PDF-'))

    for keyword in ['obj', 'endobj', 'stream', 'endstream', 'xref', 'trailer', 'startxref']:
        features[keyword] = data_str.count(keyword)

    features['pageno'] = num_pages
    features['encrypt'] = data_str.count('/Encrypt')
    features['ObjStm'] = data_str.count('/ObjStm')
    features['JS'] = data_str.count('/JS')
    features['Javascript'] = data_str.count('/JavaScript')
    features['AA'] = data_str.count('/AA')
    features['OpenAction'] = data_str.count('/OpenAction')
    features['Acroform'] = data_str.count('/AcroForm')
    features['JBIG2Decode'] = data_str.count('/JBIG2Decode')
    features['RichMedia'] = data_str.count('/RichMedia')
    features['launch'] = data_str.count('/Launch')
    features['EmbeddedFile'] = data_str.count('/EmbeddedFile')
    features['XFA'] = data_str.count('/XFA')
    features['Colors'] = data_str.count('/ColorSpace')
    features['Class'] = 0  # Placeholder

    if feature_list:
        return {key: features.get(key, 0) for key in feature_list}
    else:
        return features
