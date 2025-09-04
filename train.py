import os 
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

def append_to_file(filename, *args):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a') as file:
        for value in args:
            file.write(str(value) + '\n')

def train_model():
    # Load dataset from SageMaker input path
    input_path = os.path.join("/opt/ml/input/data/train", "insurance_pre.csv")
    
    if not os.path.exists(input_path):
        print(f"Training skipped, Reason file {input_path} is not found.")
        return
    
    df = pd.read_csv(input_path)
    
    # Split features and label
    X = df.drop("charges", axis=1)
    y = df["charges"]
    
    # one-hot encode categorical variables and drop first category
    X = pd.get_dummies(X, drop_first=True)
    print("After Get Dummies column names are:", X.columns.tolist())
    
    # Handle any missing values 
    X = X.fillna(0)
    y = y.fillna(0)
    
    # Split training and testing data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a random forest regressor
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    
    # predict on X_test values
    y_pred = model.predict(X_test)
    
    # Find out r2 values - find the evaluation metrics prediction on y_test values
    r2 = r2_score(y_test, y_pred)
    print("R2 Values :", r2)
    
    # Save model
    joblib.dump(model, os.path.join("/opt/ml/model", "model.joblib"))
    print("Model saved successfully!")

# only run this when it's a training job
if __name__ == "__main__":
    train_model()