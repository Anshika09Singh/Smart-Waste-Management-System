from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import io
import os
import json

app = Flask(__name__)
CORS(app)

# ✅ Load both models
model_paths = {
    "latest": "trash_classifier.h5",
    "best":  "best_trash_classifier.h5"
}

models = {}
for name, path in model_paths.items():
    if os.path.exists(path):
        models[name] = load_model(path)
        print(f"✅ Loaded {name} model from {path}")
    else:
        print(f"⚠️ Model not found: {path}")

# ✅ Load class indices (if available)
if os.path.exists("../class_indices.json"):
    with open("../class_indices.json", "r") as f:
        class_indices = json.load(f)
    classes = {v: k for k, v in class_indices.items()}
else:
    # fallback (manual labels, only if class_indices.json missing)
    classes = {0: 'cardboard', 1: 'glass', 2: 'metal', 3: 'paper', 4: 'plastic', 5: 'trash'}

# ✅ Dummy fill level model (replace with real DB later)
fill_data = pd.DataFrame({
    'hour': np.arange(0, 240),
    'bin1': np.random.randint(0, 100, 240),
    'bin2': np.random.randint(0, 100, 240)
})
fill_model = RandomForestRegressor()
fill_model.fit(fill_data[['hour']], fill_data['bin1'])

@app.route('/classify', methods=['POST'])
def classify_trash():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    # Select model (default = latest)
    model_choice = request.form.get("model", "latest")
    if model_choice not in models:
        return jsonify({"error": f"Invalid model choice. Available: {list(models.keys())}"}), 400

    file = request.files['file']

    # Convert FileStorage to BytesIO for Keras
    img = image.load_img(io.BytesIO(file.read()), target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred_probs = models[model_choice].predict(img_array)
    pred_idx = np.argmax(pred_probs)
    confidence = float(np.max(pred_probs))

    return jsonify({
        'model_used': model_choice,
        'class': classes[pred_idx],
        'confidence': confidence
    })

@app.route('/predict_fill', methods=['GET'])
def predict_fill():
    future_hours = pd.DataFrame({'hour': np.arange(240, 264)})
    predictions = fill_model.predict(future_hours)
    return jsonify({'predictions': predictions.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
