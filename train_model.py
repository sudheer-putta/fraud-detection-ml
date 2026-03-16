import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE

from feature_engineering import feature_engineering


# Load dataset
df = pd.read_csv("Dataset/Fraud_Analysis_Dataset.csv")


# split features and target
X = df.drop("isFraud", axis=1)
y = df["isFraud"]


X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42

)


# feature engineering transformer
feature_engineering_transformer = FunctionTransformer(
    feature_engineering,
    validate=False
)

# detect feature types
temp_df = feature_engineering(X_train)

categorical_features = temp_df.select_dtypes(include="object").columns.tolist()
numerical_features = temp_df.select_dtypes(exclude="object").columns.tolist()


# preprocessing
preprocessor = ColumnTransformer(

    transformers=[

        ("num", StandardScaler(), numerical_features),

        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)

    ]

)


# pipeline
pipeline = ImbPipeline(

    steps=[

        ("feature_engineering", feature_engineering_transformer),

        ("preprocessing", preprocessor),

        ("smote", SMOTE(random_state=42)),

        ("model", RandomForestClassifier(n_estimators=200, random_state=42))

    ]

)


# train model
pipeline.fit(X_train, y_train)


# evaluate
preds = pipeline.predict(X_test)

print(classification_report(y_test, preds))


# save model
pickle.dump(

    pipeline,
    open("fraud_pipeline.pkl","wb")

)