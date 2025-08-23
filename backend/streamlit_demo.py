import streamlit as st
import requests
from PIL import Image
import io
import pandas as pd
import json
import time

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

    st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <svg class="stSvg" width="100" height="100" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                <path d="M18 10a.5.5 0 01-.5-.5V8.293L15.207 6H13V4h3.5L19 7.5v2a.5.5 0 01-.5.5zm-12 0a.5.5 0 01-.5-.5V7.5L8.5 4H12v2h-2.207L7 8.293V9.5a.5.5 0 01-.5.5z"/>
            </svg>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🌱 Sustainable Tip of the Day"):
        st.write("Did you know that recycling a single aluminum can saves enough energy to power a television for three hours?")

    st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <p style="font-style: italic; color: #adb5bd;">
                "The greatest threat to our planet is the belief that someone else will save it."
                <br>- Robert Swan
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.info("Navigate using the sidebar to explore different features.")

# --- Trash Classification ---
if page == "Trash Classification":
    st.header("🗑️ Trash Classification")
    st.markdown("<p style='text-align:center; color:#adb5bd;'>Upload an image of a waste item for AI classification.</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload an image of trash", type=['png','jpg','jpeg'])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Trash Image", use_container_width=True)
        if st.button("Classify Trash"):
            with st.spinner('AI is classifying the trash...'):
                time.sleep(2)
                predicted_class = "Recyclable"
                confidence = 0.92
                st.markdown(f"""
                    <div class="result-card">
                        <h3>Prediction Result</h3>
                        <p style="font-size: 1.2rem;">**Class:** <span style="color: #2ecc71;">{predicted_class.upper()}</span></p>
                        <p style="font-size: 1.2rem;">**Confidence:** <span style="color: #2ecc71;">{confidence:.2f}</span></p>
                    </div>
                """, unsafe_allow_html=True)
                if "recyclable" in predicted_class.lower():
                    st.info("This item is recyclable! ♻️")
                elif "compostable" in predicted_class.lower():
                    st.info("This item is compostable. 🌱")
                else:
                    st.warning("This item is general waste. 🚮")

# --- Bin Fill Prediction ---
if page == "Bin Fill Prediction":
    st.header("📊 Predicted Bin Fill Levels")
    bins_data = {
        "Bin A": {"fill_level": 75, "prediction": 90},
        "Bin B": {"fill_level": 40, "prediction": 55},
        "Bin C": {"fill_level": 95, "prediction": 98}
    }
    df = pd.DataFrame(bins_data).T
    df.index.name = "Bin"

    st.subheader("Current & Predicted Fill Levels")
    col1, col2, col3 = st.columns(3)
    for idx, bin_name in enumerate(df.index):
        with [col1, col2, col3][idx]:
            st.subheader(bin_name)
            st.write(f"Current: {df.loc[bin_name,'fill_level']}%")
            st.progress(df.loc[bin_name,'fill_level']/100)
            st.write(f"Predicted: {df.loc[bin_name,'prediction']}%")

    st.subheader("Bin Fill History (Example Data)")
    chart_data = pd.DataFrame({
        "time": range(10),
        "Bin A": [10, 15, 20, 30, 45, 60, 70, 75, 80, 85],
        "Bin B": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        "Bin C": [2, 5, 10, 15, 25, 35, 50, 60, 75, 95]
    })
    st.line_chart(chart_data.set_index('time'))

    st.subheader("Prediction Data")
    st.dataframe(df)
    csv = df.to_csv().encode('utf-8')

    # Unique download button key
    st.download_button(
        label="Download Prediction Data as CSV",
        data=csv,
        file_name='bin_fill_predictions.csv',
        mime='text/csv',
        key='bin_fill_download_1'
    )

    # Live predictions button
    if st.button("Fetch Live Predictions"):
        try:
            response = requests.get("http://127.0.0.1:5000/predict_fill")
            if response.status_code == 200:
                live_data = response.json().get('predictions', [])
                if live_data:
                    live_df = pd.DataFrame(live_data)
                    if 'bin' in live_df.columns: live_df.set_index('bin', inplace=True)
                    st.dataframe(live_df)
                    st.line_chart(live_df)
                    csv_live = live_df.to_csv().encode('utf-8')
                    st.download_button(
                        label="Download Live Predictions CSV",
                        data=csv_live,
                        file_name='bin_fill_live_predictions.csv',
                        mime='text/csv',
                        key='bin_fill_download_2'
                    )
                else:
                    st.warning("No predictions received from API.")
            else:
                st.error(f"Error from Flask server: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Flask server not running.")
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
        ("AI-Powered Classification","Instantly identify and sort waste."),
        ("Real-Time Monitoring","Monitor bin fill levels in real-time."),
        ("Predictive Analytics","Predict bin fill patterns and optimize collection.")
    ]
    for col, (title,text) in zip([col1,col2,col3], feature_cards):
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
    team = [("Anshika Singh","AI/ML & Web Developer"), ("Shreya Sharma","Frontend Developer")]
    for col, (name,role) in zip([col1,col2], team):
        with col:
            st.markdown(f"<div class='card'><h3>{name}</h3><p>{role}</p></div>", unsafe_allow_html=True)
