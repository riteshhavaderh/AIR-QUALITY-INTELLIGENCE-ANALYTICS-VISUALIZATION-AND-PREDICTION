# =========================================================
# IMPORT LIBRARIES
# =========================================================

import streamlit as st
import pandas as pd
import joblib

# =========================================================
# LOAD SAVED FILES
# =========================================================

model = joblib.load('Models/aqi_model.pkl')

ohe = joblib.load('Models/city_encoder.pkl')

scaler = joblib.load('Models/scaler.pkl')

model_columns = joblib.load('Models/model_columns.pkl')

# =========================================================
# TITLE
# =========================================================

st.title("🌍 AQI Prediction App")

st.write(
    "Predict Air Quality Index (AQI) using pollution parameters"
)

# =========================================================
# USER INPUTS
# =========================================================

city = st.selectbox('Select City', ohe.categories_[0])

date = st.date_input('Select Date')

pm25 = st.number_input('PM2.5',min_value=0.0,value=180.0)

pm10 = st.number_input('PM10',min_value=0.0,value=320.0)

no = st.number_input('NO',min_value=0.0,value=45.0)

no2 = st.number_input('NO2',min_value=0.0,value=60.0)

nox = st.number_input('NOx',min_value=0.0,value=120.0)

nh3 = st.number_input('NH3',min_value=0.0,value=35.0)

co = st.number_input('CO',min_value=0.0,value=2.1)

so2 = st.number_input('SO2',min_value=0.0,value=18.0)

o3 = st.number_input('O3',min_value=0.0,value=55.0)

benzene = st.number_input('Benzene',min_value=0.0,value=12.0)

toluene = st.number_input('Toluene',min_value=0.0,value=20.0)

xylene = st.number_input('Xylene', min_value=0.0,value=5.0)


# =========================================================
# CREATE INPUT DATAFRAME
# =========================================================

input_data = {

    'City': [city],

    'PM2.5': [pm25],

    'PM10': [pm10],

    'NO': [no],

    'NO2': [no2],

    'NOx': [nox],

    'NH3': [nh3],

    'CO': [co],

    'SO2': [so2],

    'O3': [o3],

    'Benzene': [benzene],

    'Toluene': [toluene],

    'Xylene': [xylene],

    'Date': [str(date)]

}

# Convert dictionary to DataFrame
input_df = pd.DataFrame(input_data)


# =========================================================
# PROCESS DATE
# =========================================================

input_df['Date'] = pd.to_datetime(input_df['Date'])

input_df['Year'] = input_df['Date'].dt.year

input_df['Month'] = input_df['Date'].dt.month

input_df['Weekday'] = input_df['Date'].dt.weekday

# Drop Date column
input_df.drop('Date', axis=1, inplace=True)

# =========================================================
# APPLY ONE HOT ENCODING
# =========================================================

city_encoded = ohe.transform(input_df[['City']])

city_df = pd.DataFrame(

    city_encoded,

    columns=ohe.get_feature_names_out(['City'])

)

# Drop original city column
input_df.drop('City', axis=1, inplace=True)

# Add encoded columns
input_df = pd.concat(

    [input_df, city_df],

    axis=1

)

# =========================================================
# MATCH TRAINING COLUMNS
# =========================================================

input_df = input_df.reindex(

    columns=model_columns,

    fill_value=0

)


# =========================================================
# APPLY SCALING
# =========================================================

input_scaled = scaler.transform(input_df)


# =========================================================
# PREDICT
# =========================================================

if st.button('Predict AQI Bucket'):

    prediction = model.predict(input_scaled)

    predicted_aqi_bucket = prediction[0]

    st.success(
        f'Predicted AQI Category : {predicted_aqi_bucket}'
    )