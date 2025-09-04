import pandas as pd
import json
import numpy as np
import io
import os
import joblib
import logging


logging.basicConfig(level=logging.INFO)

# Load the trained model
def model_fn(model_dir):
    model_path = os.path.join(model_dir, "model.joblib")
    logging.info(f"Loading model from {model_path}")
    return joblib.load(model_path)

# Parse input
def input_fn(request_body, content_type):
    logging.info(f"Received content type: {content_type}")
    logging.info(f"Request body: {request_body}")

    if content_type == "application/json":
        data_dict = json.loads(request_body)
        df = pd.DataFrame(data_dict)
        logging.info(f"Input DataFrame shape: {df.shape}")
        return df
    elif content_type == "application/x-npy":
        array = np.load(io.BytesIO(request_body))
        df = pd.DataFrame(array)
        logging.info(f"Input NPY DataFrame shape: {df.shape}")
        return df
    else:
        raise ValueError(f"Unsupported content type {content_type}")

# Prediction
def predict_fn(input_data, model):
    logging.info("Running prediction...")
    predictions = model.predict(input_data)
    logging.info(f"Predictions: {predictions}")
    return predictions

# Format output
def output_fn(prediction, content_type):
    logging.info("Formatting output...")
    return json.dumps(prediction.tolist())
