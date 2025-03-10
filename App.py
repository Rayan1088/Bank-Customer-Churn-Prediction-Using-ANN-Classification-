import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

# Load the model
model = tf.keras.models.load_model('Updated_ANN_classification_model.h5')

# Load the encoders and scaler
with open('lable_Encoding_gender.pkl', 'rb') as file:
    label_encoder_gender = pickle.load(file)

with open('One_Hot_Encoding_Geography.pkl', 'rb') as file:
    one_hot_encoder_geography = pickle.load(file)    
    
with open('Feature_scaling.pkl', 'rb') as file:
    feature_scaler = pickle.load(file)   
    
# Streamlit App
st.title('Estimated Salary Prediction')

# Input Features

geography=st.selectbox('Geography', one_hot_encoder_geography.columns.tolist())
gender=st.selectbox('Gender', label_encoder_gender.classes_)

age=st.number_input('Age', min_value=18, max_value=100)
balance=st.number_input('Balance')  
credit_score=st.number_input('Credit Score')
estimated_salary=st.number_input('Estimated Salary')
num_of_products=st.number_input('Number of Products')

tenure=st.slider('Tenure',0,10)

has_credit_card=st.selectbox('Has Credit Card', [0,1], format_func=lambda x: 'Yes' if x == 1 else 'No')
is_active_member=st.selectbox('Is Active Member', [0,1], format_func=lambda x: 'Yes' if x == 1 else 'No')


# Prepare the input features
input_features_df = pd.DataFrame({'CreditScore': [credit_score],
                                'Gender' : [label_encoder_gender.transform([gender])[0]],
                                'Age': [age],
                                'Tenure': [tenure],
                                'Balance': [balance],
                                'NumOfProducts': [num_of_products],
                                'HasCrCard': [has_credit_card],
                                'IsActiveMember': [is_active_member],
                                'EstimatedSalary': [estimated_salary]
                                 })

# One hot encoding for Geography
geography_encoded = pd.DataFrame(0, index=[0], columns=one_hot_encoder_geography.columns)
geography_encoded.loc[0, geography] = 1

# Concatenate the input features and geography_encoded_df 
input_features_df = pd.concat([input_features_df, geography_encoded], axis=1)

# Feature scaling
scaled_input_features = feature_scaler.transform(input_features_df)        

# Predict the churn
prediction = model.predict(scaled_input_features)
The_Probabilistic_Value_of_prediction = prediction[0][0]

if st.button('Predict Churn'):
    if The_Probabilistic_Value_of_prediction > 0.5:
        st.write("The Customer will leave the Bank")
    else:
        st.write("The Customer will not leave the Bank")   