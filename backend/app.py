from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import io

app = Flask(__name__)
CORS(app)


trash_model = load_model('models/trash_classifier.h5')


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
    
    file = request.files['file']
    
    # Convert FileStorage to BytesIO for Keras
    img = image.load_img(io.BytesIO(file.read()), target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = np.argmax(trash_model.predict(img_array))
    classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
    
    return jsonify({'class': classes[pred]})


@app.route('/predict_fill', methods=['GET'])
def predict_fill():
    future_hours = pd.DataFrame({'hour': np.arange(240, 264)})
    predictions = fill_model.predict(future_hours)
    return jsonify({'predictions': predictions.tolist()})


if __name__ == '__main__':
    app.run(debug=True)
