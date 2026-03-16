import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from feature_engineering import feature_engineering

print("FastAPI running at: http://localhost:8000/docs")

model = pickle.load(open("fraud_pipeline.pkl", "rb"))

app = FastAPI()

# Allow CORS from anywhere for simple local/dev usage (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Transaction(BaseModel):
    step: int
    type: str
    amount: float
    nameOrig: str
    oldbalanceOrg: float
    newbalanceOrig: float
    nameDest: str
    oldbalanceDest: float
    newbalanceDest: float


@app.get("/")
def home():
    return {"message": "Fraud Detection API Running"}


@app.post("/predict")
def predict(data: Transaction):

    try:
        # Support both pydantic v2 (model_dump) and v1 (dict)
        try:
            data_dict = data.model_dump()
        except Exception:
            data_dict = data.dict()

        df = pd.DataFrame([data_dict])

        prediction = model.predict(df)[0]

        return {
            "prediction": int(prediction),
            "result": "Fraud" if int(prediction) == 1 else "Not Fraud"
        }

    except Exception as e:
        # Return proper HTTP 500 with error message for easier debugging
        raise HTTPException(status_code=500, detail=str(e))