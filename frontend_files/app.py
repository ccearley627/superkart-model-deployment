import os
import pandas as pd
import requests
import streamlit as st

BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:7860')
st.set_page_config(page_title='SuperKart Sales Forecast', page_icon='🛒')
st.title('SuperKart Sales Forecast')
st.write('Enter product and store attributes to estimate product-store sales revenue.')

product_data = {
    'Product_Weight': st.number_input('Product Weight', min_value=0.0, value=12.66),
    'Product_Sugar_Content': st.selectbox('Product Sugar Content', ['Low Sugar', 'Regular', 'No Sugar']),
    'Product_Allocated_Area': st.number_input('Product Allocated Area', min_value=0.0, value=0.027, format='%.3f'),
    'Product_MRP': st.number_input('Product MRP', min_value=0.0, value=117.08),
    'Store_Size': st.selectbox('Store Size', ['Small', 'Medium', 'High']),
    'Store_Location_City_Type': st.selectbox('Store Location City Type', ['Tier 1', 'Tier 2', 'Tier 3']),
    'Store_Type': st.selectbox('Store Type', ['Supermarket Type1', 'Supermarket Type2', 'Departmental Store', 'Food Mart']),
    'Product_Id_char': st.selectbox('Product ID Prefix', ['FD', 'DR', 'NC']),
    'Store_Age_Years': st.number_input('Store Age in Years', min_value=0, value=16),
    'Product_Type_Category': st.selectbox('Product Type Category', ['Perishables', 'Non Perishables']),
}

if st.button('Predict sales', type='primary'):
    response = requests.post(f'{BACKEND_URL}/v1/predict', json=product_data, timeout=30)
    if response.ok:
        st.success(f"Predicted Product Store Sales Total: ₹{response.json()['Sales']:,.2f}")
    else:
        st.error(response.text)

st.subheader('Batch prediction')
uploaded_file = st.file_uploader('Upload a CSV file', type=['csv'])
if uploaded_file is not None and st.button('Predict batch'):
    response = requests.post(f'{BACKEND_URL}/v1/predictbatch', files={'file': uploaded_file}, timeout=60)
    if response.ok:
        results = response.json()
        st.success('Predictions completed successfully')
        st.dataframe(pd.DataFrame({'Row': list(results.keys()), 'Predicted Sales': list(results.values())}), use_container_width=True)
    else:
        st.error(response.text)
