import streamlit as st
import requests
import os

print("Streamlit running at: http://localhost:8501")

st.title("💳 Fraud Detection System")
st.write("Enter transaction details")

step = st.number_input("Step", value=1)
type_txn = st.selectbox("Transaction Type",
                        ["PAYMENT","TRANSFER","CASH_OUT","DEBIT","CASH_IN"])

amount = st.number_input("Amount", value=1000)

oldbalanceOrg = st.number_input("Old Balance Origin", value=10000)
newbalanceOrig = st.number_input("New Balance Origin", value=9000)

oldbalanceDest = st.number_input("Old Balance Destination", value=0)
newbalanceDest = st.number_input("New Balance Destination", value=0)

nameOrig = st.text_input("Sender ID", "C123")
nameDest = st.text_input("Receiver ID", "C456")

if st.button("Predict Fraud"):

    data = {
        "step": step,
        "type": type_txn,
        "amount": amount,
        "nameOrig": nameOrig,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "nameDest": nameDest,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }

    # API URL can be configured via environment variable API_URL.
    # Default to localhost for local runs. When running with docker-compose
    # set API_URL to http://api:8000/predict so the streamlit container can reach the api service.
    api_url = os.environ.get("API_URL", "http://localhost:8000/predict")

    try:
        response = requests.post(api_url, json=data, timeout=10)

        # Debug output
        st.write("Status Code:", response.status_code)
        st.write("Raw Response:", response.text)

        if response.status_code == 200:
            result = response.json()
            st.success(result.get("result", "No result field"))
        else:
            # Show returned error message if any
            try:
                err = response.json()
            except Exception:
                err = response.text
            st.error(f"API error occurred: {err}")

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to reach API at {api_url}: {e}")