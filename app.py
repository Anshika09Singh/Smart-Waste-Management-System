# app.py  —— Single-file Streamlit + Flask (merged)
import os
import io
import time
import threading
import requests
import numpy as np
import pandas as pd
from PIL import Image

# ====== Flask backend (runs in background thread) ======
from flask import Flask, request, jsonify
from flask_cors import CORS

# Optional: silence TF logs a bit
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing import image as keras_image
    TF_AVAILABLE = True
except Exception:
    TF_AVAILABLE = False

from sklearn.ensemble import RandomForestRegressor

flask_app = Flask(__name__)
CORS(flask_app)

# --- Models / data used by Flask routes ---
TRASH_CLASSES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
trash_model = None
fill_model = None

def _load_trash_model():
    global trash_model
    if not TF_AVAILABLE:
        trash_model = None
        return
    model_path = os.path.join("models", "trash_classifier.h5")
    if os.path.exists(model_path):
        trash_model = load_model(model_path)
    else:
        trash_model = None

def _train_fill_model():
    global fill_model
    fill_data = pd.DataFrame({
        'hour': np.arange(0, 240),
        'bin1': np.random.randint(0, 100, 240),
        'bin2': np.random.randint(0, 100, 240)
    })
    fill_model = RandomForestRegressor()
    fill_model.fit(fill_data[['hour']], fill_data['bin1'])

@flask_app.route('/classify', methods=['POST'])
def classify_trash():
    if 'file' not in request.files and 'url' not in request.form:
        return jsonify({'error': 'No file or url provided'}), 400

    img_bytes = None
    if 'file' in request.files:
        img_bytes = request.files['file'].read()
    elif 'url' in request.form:
        try:
            r = requests.get(request.form['url'], timeout=10)
            r.raise_for_status()
            img_bytes = r.content
        except Exception as e:
            return jsonify({'error': f'Failed to fetch URL: {e}'}), 400

    if img_bytes is None:
        return jsonify({'error': 'No image data'}), 400

    # If no model, return a friendly fallback (so UI still works)
    if trash_model is None:
        return jsonify({'class': 'unknown', 'note': 'Model not found or TF unavailable'}), 200

    # Preprocess
    img = keras_image.load_img(io.BytesIO(img_bytes), target_size=(128, 128))
    img_array = keras_image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = trash_model.predict(img_array)
    pred_idx = int(np.argmax(preds))
    return jsonify({'class': TRASH_CLASSES[pred_idx]}), 200

@flask_app.route('/predict_fill', methods=['GET'])
def predict_fill():
    if fill_model is None:
        return jsonify({'predictions': []}), 200
    future_hours = pd.DataFrame({'hour': np.arange(240, 264)})
    predictions = fill_model.predict(future_hours)
    # Return as time series with an index label to make plotting easy in Streamlit
    return jsonify({
        'predictions': [
            {'time': int(t), 'Bin A': float(v)}
            for t, v in zip(future_hours['hour'], predictions)
        ]
    }), 200

def run_flask_background():
    # load models once
    _load_trash_model()
    _train_fill_model()
    # Important: use_reloader=False or Streamlit will spawn multiple Flask servers
    flask_app.run(host='127.0.0.1', port=8000, debug=False, use_reloader=False)

# ====== Start Flask thread once ======
_FLASK_STARTED = False
def ensure_flask_running():
    global _FLASK_STARTED
    if not _FLASK_STARTED:
        t = threading.Thread(target=run_flask_background, daemon=True)
        t.start()
        _FLASK_STARTED = True
        # tiny wait to let the server bind
        time.sleep(0.5)

# ====== Streamlit Frontend ======
import streamlit as st

# Start backend
ensure_flask_running()

# --- CSS Styling for a Modern Dark Look & Responsiveness ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; padding-left: 5%; padding-right: 5%; }
    .stApp { background-color: #212529; color: #f8f9fa; }
    h1, h2, h3, h4, h5, h6, .stMarkdown, p, label { color: #f8f9fa !important; }
    .hero-container { padding: 5rem 0; background-color: #2c3034; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); text-align: center; margin-bottom: 2rem; position: relative; overflow: hidden; }
    .hero-container h1 { font-size: 3rem; font-weight: 700; color: #2ecc71 !important; }
    .hero-container p { font-size: 1.25rem; color: #adb5bd !important; max-width: 600px; margin: 0 auto; }
    [data-testid="stSidebar"] { background: #2c3034; border-right: 1px solid #495057; box-shadow: 2px 0 10px rgba(0,0,0,0.2); }
    [data-testid="stSidebarNav"] li a { font-size: 1rem; font-weight: 600; color: #f8f9fa; transition: all 0.3s ease; padding: 1rem; border-radius: 8px; }
    [data-testid="stSidebarNav"] li a:hover { background-color: #495057; color: #00bfff; transform: translateX(5px); }
    [data-testid="stSidebarNav"] li a[aria-selected="true"] { background-color: #007bff; color: white; transform: translateX(0); box-shadow: 0 2px 10px rgba(0, 123, 255, 0.2); }
    .card { background-color: #2c3034; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); padding: 2rem; text-align: center; transition: transform 0.3s ease, box-shadow 0.3s ease; height: 100%; }
    .card:hover { transform: translateY(-10px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
    .card h3 { color: #f8f9fa !important; font-weight: 600; }
    .card p { color: #adb5bd !important; }
    .result-card { background-color: #343a40; border-left: 5px solid #2ecc71; padding: 1.5rem; border-radius: 8px; margin-top: 1rem; }
    .stButton>button { background-color: #007bff; color: white; border: none; border-radius: 8px; padding: 10px 20px; box-shadow: 0 4px 10px rgba(0,123,255,0.2); transition: transform 0.2s ease, box-shadow 0.2s ease; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .stButton>button:hover { background-color: #0056b3; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,123,255,0.3); }
    [data-testid="stFileUploaderDropzone"] { background-color: #2c3034; border: 2px dashed #007bff; border-radius: 10px; padding: 2rem; transition: background-color 0.3s ease, border-color 0.3s ease; }
    [data-testid="stFileUploaderDropzone"] p { color: #adb5bd; }
    [data-testid="stFileUploaderDropzone"]:hover { background-color: #3b4045; border-color: #00bfff; }
    .stProgress > div > div > div > div { background-color: #28a745 !important; }
    .stProgress > div > div > div { background-color: #495057; }
    h2, .stMarkdown h2 { color: #f8f9fa !important; border-bottom: 2px solid #495057; padding-bottom: 0.5rem; margin-top: 2rem; }
    img { max-width: 100%; height: auto; border-radius: 10px; }
    .stSvg { animation: pulse-and-fade 2s infinite ease-in-out; }
    @keyframes pulse-and-fade { 0% { transform: scale(0.8); opacity: 0.5; } 50% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(0.8); opacity: 0.5; } }
    .stSvg circle { fill: #2ecc71; }
    .stSvg path { fill: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("Smart Waste ♻️")
st.sidebar.subheader("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Trash Classification", "Bin Fill Prediction", "Sustainable Tips", "Features", "About"])

# --- Home Page ---


if page == "Home":
    st.markdown("""
        <div class="hero-container">
            <h1 style="color:#2ecc71;">Smart Waste Management</h1>
            <p style="color:#adb5bd;">Leveraging AI to classify trash and predict bin fill levels for a cleaner, smarter city.</p>
        </div>
    """, unsafe_allow_html=True)

    # --- Centered Home Page Image ---
    image_url = "https://tse1.mm.bing.net/th/id/OIP.DxyrzKD7X8eYtxotGlV2vwAAAA?cb=thfc1&rs=1&pid=ImgDetMain&o=7&rm=3"
    try:
        response = requests.get(image_url)
        img = Image.open(io.BytesIO(response.content))
        st.image(img, caption="Keep Future Bright", use_container_width=True)
    except Exception as e:
        st.warning(f"Could not load image: {e}")

    st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <svg class="stSvg" width="10" height="10" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                <path d="M18 10a.5.5 0 01-.5-.5V8.293L15.207 6H13V4h3.5L19 7.5v2a.5.5 0 01-.5.5zm-12 0a.5.5 0 01-.5-.5V7.5L8.5 4H12v2h-2.207L7 8.293V9.5a.5.5 0 01-.5.5z"/>
            </svg>
        </div>
    """, unsafe_allow_html=True)

    st.info("Use the sidebar to explore features.")

    

    # with st.expander("🌱 Sustainable Tip of the Day"):
    #     st.write("Recycling a single aluminum can saves enough energy to power a TV for ~3 hours.")

    # st.info("Use the sidebar to explore features.")
    

# --- Trash Classification ---
if page == "Trash Classification":
    st.header("🗑️ Trash Classification")
    st.markdown("<p style='text-align:center; color:#adb5bd;'>Upload an image OR paste an image URL (e.g., Google Images) for AI classification.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Upload Image", "Image URL"])
    uploaded_file = None
    image_url = None

    with tab1:
        uploaded_file = st.file_uploader("Upload an image (png/jpg/jpeg)", type=['png','jpg','jpeg'])
        if uploaded_file:
            st.image(uploaded_file, caption="Preview", use_container_width=True)

    with tab2:
        image_url = st.text_input("Paste image URL")
        if image_url:
            try:
                r = requests.get(image_url, timeout=10)
                r.raise_for_status()
                st.image(r.content, caption="Preview from URL", use_container_width=True)
            except Exception as e:
                st.warning(f"Could not load image from URL: {e}")

    if st.button("Classify Trash"):
        with st.spinner('AI is classifying the trash...'):
            try:
                if uploaded_file:
                    files = {"file": uploaded_file.getvalue()}
                    resp = requests.post("http://127.0.0.1:8000/classify", files=files, timeout=30)
                elif image_url:
                    data = {"url": image_url}
                    resp = requests.post("http://127.0.0.1:8000/classify", data=data, timeout=30)
                else:
                    st.error("Please upload an image or provide an image URL.")
                    resp = None

                if resp is not None:
                    if resp.status_code == 200:
                        result = resp.json()
                        predicted_class = result.get("class", "unknown")
                        st.markdown(f"""
                            <div class="result-card">
                                <h3>Prediction Result</h3>
                                <p style="font-size: 1.2rem;">Class: <span style="color: #2ecc71;">{predicted_class.upper()}</span></p>
                            </div>
                        """, unsafe_allow_html=True)

                        # Contextual hints
                        low = predicted_class.lower()
                        if low in ["cardboard", "paper"]:
                            st.info("This item is recyclable! ♻️")
                        elif low in ["metal", "glass"]:
                            st.info("This material can be recycled efficiently. 🔄")
                        elif low == "plastic":
                            st.warning("Plastic detected. Recycle responsibly. 🚯")
                        elif low == "unknown":
                            st.warning("Model not loaded. Check model path or TensorFlow install.")
                        else:
                            st.error("This seems like general waste. 🚮")
                    else:
                        st.error(f"Backend error: {resp.text}")
            except requests.exceptions.ConnectionError:
                st.error("Flask server not reachable (started in background). Try rerunning the app.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# --- Bin Fill Prediction ---
if page == "Bin Fill Prediction":
    st.header("📊 Predicted Bin Fill Levels")
    # Example current levels
    bins_data = {
        "Bin A": {"fill_level": 75, "prediction": 90},
        "Bin B": {"fill_level": 40, "prediction": 55},
        "Bin C": {"fill_level": 95, "prediction": 98}
    }
    df = pd.DataFrame(bins_data).T
    df.index.name = "Bin"

    st.subheader("Current & Predicted Fill Levels")
    cols = st.columns(len(df))
    for idx, bin_name in enumerate(df.index):
        with cols[idx]:
            st.subheader(bin_name)
            st.write(f"Current: {df.loc[bin_name,'fill_level']}%")
            st.progress(df.loc[bin_name,'fill_level']/100)
            st.write(f"Predicted: {df.loc[bin_name,'prediction']}%")

    st.subheader("Fetch Live Predictions (from embedded Flask)")
    if st.button("Fetch Live Predictions"):
        try:
            response = requests.get("http://127.0.0.1:8000/predict_fill", timeout=20)
            if response.status_code == 200:
                data = response.json().get('predictions', [])
                if data:
                    live_df = pd.DataFrame(data).set_index('time')
                    st.dataframe(live_df)
                    st.line_chart(live_df)  # uses use_container_width by default
                else:
                    st.warning("No predictions returned.")
            else:
                st.error(f"Error from backend: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Flask server not reachable.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# --- Sustainable Tips ---
if page == "Sustainable Tips":
    st.header("💡 Sustainable Living Tips")
    tips = {
        "Compost": "Start a compost bin for your food scraps.",
        "Reusable Bags": "Bring your own reusable bags when shopping.",
        "Repair, Don't Replace": "Try to fix broken items first.",
        "Reduce Paper": "Go paperless whenever possible.",
        "Mindful Consumption": "Buy only what you need."
    }
    for title, text in tips.items():
        st.markdown(f"""
        <div class="card" style="margin-bottom: 1.5rem;">
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """, unsafe_allow_html=True)

# --- Features ---
if page == "Features":
    st.header("✨ Key Features")
    col1, col2, col3 = st.columns(3)
    feature_cards = [
        ("AI-Powered Classification", "Instantly identify and sort waste."),
        ("Real-Time Monitoring", "Monitor bin fill levels in real-time."),
        ("Predictive Analytics", "Predict bin fill patterns and optimize collection.")
    ]
    for col, (title, text) in zip([col1, col2, col3], feature_cards):
        with col:
            st.markdown(f"""
            <div class="card">
                <h3>{title}</h3>
                <p>{text}</p>
            </div>
            """, unsafe_allow_html=True)

# --- About ---
if page == "About":
    st.header("ℹ️ About Us")
    st.markdown("<p style='text-align:center; color:#adb5bd;'>We aim to revolutionize waste collection with a sustainable future in mind.</p>", unsafe_allow_html=True)
    st.subheader("Meet the Team")
    col1, col2 = st.columns(2)
    team = [("Anshika Singh", "AI/ML & Web Developer"), ("Shreya Sharma", "Frontend Developer")]
    for col, (name, role) in zip([col1, col2], team):
        with col:
            st.markdown(f"<div class='card'><h3>{name}</h3><p>{role}</p></div>", unsafe_allow_html=True)
