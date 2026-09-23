from pathlib import Path
import joblib
import pandas as pd
from flask import Flask, request, jsonify

superkart_api = Flask('SuperKart')
MODEL_PATH = Path(__file__).resolve().parent / 'superkart_model.joblib'
model = joblib.load(MODEL_PATH)

@superkart_api.get('/')
def home():
    return 'Welcome to the SuperKart System'

@superkart_api.post('/v1/predict')
def predict_sales():
    data = request.get_json()
    expected = [
        'Product_Weight', 'Product_Sugar_Content', 'Product_Allocated_Area',
        'Product_MRP', 'Store_Size', 'Store_Location_City_Type', 'Store_Type',
        'Product_Id_char', 'Store_Age_Years', 'Product_Type_Category'
    ]
    missing = [field for field in expected if field not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400
    prediction = float(model.predict(pd.DataFrame([{k: data[k] for k in expected}]))[0])
    return jsonify({'Sales': round(prediction, 2)})

@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    if 'file' not in request.files:
        return jsonify({'error': 'CSV file is required'}), 400
    input_data = pd.read_csv(request.files['file'])
    predictions = model.predict(input_data)
    return jsonify({str(i): round(float(pred), 2) for i, pred in enumerate(predictions)})

if __name__ == '__main__':
    superkart_api.run(host='0.0.0.0', port=7860)
