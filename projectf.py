# -*- coding: utf-8 -*-
"""P1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1keJyxmZVBPW0jKB_d2x7SWe6ygjSFhGW
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

df=pd.read_csv('Youtube-Spam-Dataset.csv')
df.head()

# Check for missing values
df.isnull().sum()

# Drop rows with missing values
df.dropna(inplace=True)

# Distribution of spam vs non-spam comments
plt.figure(figsize=(6,4))
sns.countplot(x='CLASS', data=df)
plt.title('Distribution of Spam vs Non-Spam Comments')
plt.xlabel('Class (0: Non-Spam, 1: Spam)')
plt.ylabel('Count')
plt.show()

# Convert the 'DATE' column to datetime
df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')

# Extract features from the 'DATE' column
df['YEAR'] = df['DATE'].dt.year
df['MONTH'] = df['DATE'].dt.month
df['DAY'] = df['DATE'].dt.day
df['HOUR'] = df['DATE'].dt.hour

# Select only numeric columns for correlation analysis
numeric_df = df.select_dtypes(include=[np.number])
plt.figure(figsize=(10,8))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()

# Vectorize the 'CONTENT' column using TF-IDF
tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
X = tfidf.fit_transform(df['CONTENT'])
y = df['CLASS']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Shape of X_train: ", X_train.shape)
print("Shape of X_test: ", X_test.shape)

# Train a Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Display the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Display the classification report
print(classification_report(y_test, y_pred))


import streamlit as st
import cohere



# Initialize Cohere client
COHERE_API_KEY = 'YOUR_COHERE_API_KEY'
co = cohere.Client('pGbElaDbFkEHelKRVKyQG6QoTB14XF4iQ0iOMEqP')

# Load dataset
def load_data(file_path):
    return pd.read_csv(file_path)

# Predict function using Cohere
def predict_spam(text):
    response = co.classify(
        model='large',
        inputs=[text],
        examples=[
            cohere.classify.Example("Buy now and get 50% off!", "spam"),
            cohere.classify.Example("Check out my new video!", "spam"),
            cohere.classify.Example("This video was really helpful, thanks!", "not spam"),
            cohere.classify.Example("I loved the part where you explained the code.", "not spam")
            # Add more examples for better accuracy
        ]
    )
    return response.classifications[0].prediction

# Streamlit app
st.title('YouTube Spam Comments Detector')
st.write('Upload a CSV file containing comments and their labels.')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = load_data(uploaded_file)
    st.write(data.head())

    st.write('Predict spam for new comment:')
    user_comment = st.text_area("Enter a YouTube comment")

    if st.button('Predict'):
        if user_comment:
            prediction = predict_spam(user_comment)
            st.write(f'This comment is predicted to be: **{prediction}**')
        else:
            st.write('Please enter a comment to predict.')
else:
    st.write('Please upload a CSV file to proceed.')

# To run the app, use the following command in the terminal:
# streamlit run your_script_name.py


    st.write("Fetched Comments:")
    for comment in comments:
        is_spam = detect_spam(comment)
        st.write(f"Comment: {comment}")
        st.write(f"Spam: {'Yes' if is_spam else 'No'}")
