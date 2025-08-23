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

    .hero-container { 
        padding: 4rem 2rem; 
        background: linear-gradient(135deg, #89d957 0%, #81865e 100%); 
        border-radius: 20px; 
        box-shadow: 0 8px 32px rgba(129, 134, 94, 0.2); 
        text-align: center; 
        margin-bottom: 2rem; 
        position: relative; 
        overflow: hidden; 
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    .hero-container h1 { 
        font-size: 3rem; 
        font-weight: 700; 
        color: #ffffff !important; 
        position: relative; 
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .hero-container p { 
        font-size: 1.25rem; 
        color: #ffffff !important; 
        max-width: 600px; 
        margin: 0 auto; 
        position: relative; 
        z-index: 1;
        opacity: 0.95;
    }

    [data-testid="stSidebar"] { 
        background: #2c3034; 
        border-right: 1px solid #495057; 
        box-shadow: 2px 0 10px rgba(0,0,0,0.2); 
    }
    [data-testid="stSidebarNav"] li a { 
        font-size: 1rem; 
        font-weight: 600; 
        color: #f8f9fa; 
        transition: all 0.3s ease; 
        padding: 1rem; 
        border-radius: 8px; 
    }
    [data-testid="stSidebarNav"] li a:hover { 
        background-color: #495057; 
        color: #89d957; 
        transform: translateX(5px); 
    }
    [data-testid="stSidebarNav"] li a[aria-selected="true"] { 
        background: linear-gradient(135deg, #81865e, #89d957); 
        color: white; 
        transform: translateX(0); 
        box-shadow: 0 2px 10px rgba(129, 134, 94, 0.4); 
    }
    

    .card { 
        background-color: #2c3034; 
        border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
        padding: 2rem; 
        text-align: center; 
        transition: transform 0.3s ease, box-shadow 0.3s ease; 
        height: 100%; 
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 200px;
    }
    .card:hover { 
        transform: translateY(-10px); 
        box-shadow: 0 10px 30px rgba(0,0,0,0.3); 
    }
    .card h3 { 
        color: #f8f9fa !important; 
        font-weight: 600; 
        font-size: 1.1rem !important;
        line-height: 1.3 !important;
        margin-bottom: 0.8rem !important;
        word-wrap: break-word;
        hyphens: auto;
    }
    .card p { 
        color: #adb5bd !important; 
        font-size: 0.9rem !important;
        line-height: 1.4 !important;
        margin: 0 !important;
        word-wrap: break-word;
        hyphens: auto;
    }

    .result-card { 
        background-color: #343a40; 
        border-left: 5px solid #89d957; 
        padding: 1.5rem; 
        border-radius: 8px; 
        margin-top: 1rem; 
    }
    
    .stButton>button { 
        background: linear-gradient(135deg, #89d957 0%, #81865e 100%); 
        color: #ffffff !important; 
        border: none; 
        border-radius: 12px; 
        padding: 12px 24px; 
        box-shadow: 0 4px 15px rgba(129, 134, 94, 0.3); 
        transition: all 0.3s ease; 
        font-weight: 600; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
    }
    .stButton>button:hover { 
        background: linear-gradient(135deg, #81865e 0%, #89d957 100%); 
        transform: translateY(-2px); 
        box-shadow: 0 8px 25px rgba(129, 134, 94, 0.4); 
        color: #ffffff !important;
    }
    
    /* Download button specific styling */
    .stDownloadButton>button { 
        background: linear-gradient(135deg, #89d957 0%, #81865e 100%); 
        color: #ffffff !important; 
        border: none; 
        border-radius: 12px; 
        padding: 12px 24px; 
        box-shadow: 0 4px 15px rgba(129, 134, 94, 0.3); 
        transition: all 0.3s ease; 
        font-weight: 600; 
    }
    .stDownloadButton>button:hover { 
        background: linear-gradient(135deg, #81865e 0%, #89d957 100%); 
        color: #ffffff !important;
    }

    [data-testid="stFileUploaderDropzone"] { 
        background-color: #2c3034; 
        border: 2px dashed #89d957; 
        border-radius: 10px; 
        padding: 2rem; 
        transition: background-color 0.3s ease, border-color 0.3s ease; 
    }
    [data-testid="stFileUploaderDropzone"] p { 
        color: #adb5bd !important; 
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover { 
        background-color: #3b4045; 
        border-color: #81865e; 
    }
    
    /* File uploader text styling */
    .uploadedFile { color: #adb5bd !important; }
    [data-testid="stFileUploaderDropzoneInstructions"] { color: #adb5bd !important; }

    .stProgress > div > div > div > div { background: linear-gradient(90deg, #89d957, #81865e) !important; }
    .stProgress > div > div > div { background-color: #495057; }

    h2, .stMarkdown h2 { 
        color: #f8f9fa !important; 
        border-bottom: 2px solid #495057; 
        padding-bottom: 0.5rem; 
        margin-top: 2rem; 
    }
    img { max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }

    .stSvg { animation: pulse-and-fade 2s infinite ease-in-out; }
    @keyframes pulse-and-fade { 
        0% { transform: scale(0.9); opacity: 0.7; } 
        50% { transform: scale(1.1); opacity: 1; } 
        100% { transform: scale(0.9); opacity: 0.7; } 
    }
    .stSvg circle { fill: #89d957; }
    .stSvg path { fill: #ffffff; }
    
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("Smart Waste ♻️")
st.sidebar.subheader("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Trash Classification", "Bin Fill Prediction", "Sustainable Tips", "Features", "About"])

# --- Home Page ---
if page == "Home":
    # Dashboard Header
    st.markdown("""
        <div style="background: linear-gradient(135deg, #89d957 0%, #81865e 100%); padding: 2rem; border-radius: 20px; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700;">Smart Waste Dashboard</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">Real-time monitoring and AI-powered waste management</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="card" style="text-align: center; padding: 1.5rem;">
                <div style="background: linear-gradient(135deg, #89d957, #81865e); width: 60px; height: 60px; border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-size: 1.5rem;">🗑️</span>
                </div>
                <h3 style="color: #89d957; font-size: 2.5rem; margin: 0;">247</h3>
                <p style="color: #adb5bd; margin: 0.5rem 0 0 0; font-weight: 500;">Total Bins</p>
                <p style="color: #6c757d; margin: 0.3rem 0 0 0; font-size: 0.8rem;">+12 this month</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card" style="text-align: center; padding: 1.5rem;">
                <div style="background: linear-gradient(135deg, #89d957, #81865e); width: 60px; height: 60px; border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-size: 1.5rem;">📊</span>
                </div>
                <h3 style="color: #89d957; font-size: 2.5rem; margin: 0;">89%</h3>
                <p style="color: #adb5bd; margin: 0.5rem 0 0 0; font-weight: 500;">Efficiency Rate</p>
                <p style="color: #6c757d; margin: 0.3rem 0 0 0; font-size: 0.8rem;">+5% from last week</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card" style="text-align: center; padding: 1.5rem;">
                <div style="background: linear-gradient(135deg, #89d957, #81865e); width: 60px; height: 60px; border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-size: 1.5rem;">🚛</span>
                </div>
                <h3 style="color: #89d957; font-size: 2.5rem; margin: 0;">12</h3>
                <p style="color: #adb5bd; margin: 0.5rem 0 0 0; font-weight: 500;">Active Routes</p>
                <p style="color: #6c757d; margin: 0.3rem 0 0 0; font-size: 0.8rem;">3 optimized today</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="card" style="text-align: center; padding: 1.5rem;">
                <div style="background: linear-gradient(135deg, #89d957, #81865e); width: 60px; height: 60px; border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-size: 1.5rem;">🤖</span>
                </div>
                <h3 style="color: #89d957; font-size: 2.5rem; margin: 0;">1.2K</h3>
                <p style="color: #adb5bd; margin: 0.5rem 0 0 0; font-weight: 500;">Items Classified</p>
                <p style="color: #6c757d; margin: 0.3rem 0 0 0; font-size: 0.8rem;">156 today</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Dashboard Content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <div class="card" style="padding: 2rem; min-height: 400px;">
                <h3 style="color: #f8f9fa; margin-bottom: 1.5rem;">🗑️ Waste Classification Overview</h3>
                <img src="https://images.unsplash.com/photo-1752486920540-016b9aefee41?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" 
                style="width: 100%; height: 200px; object-fit: cover; border-radius: 12px; margin-bottom: 1rem;">
                <p style="color: #636e72; line-height: 1.6;">Our AI-powered system automatically classifies waste items into categories like plastic, metal, glass, and cardboard with 94% accuracy.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Today's Stats Card
        st.markdown("""
            <div class="card" style="padding: 1.5rem; margin-bottom: 1rem;">
                <h4 style="color: #f8f9fa; margin-bottom: 1rem; font-weight: 600;">📊 Today's Stats</h4>
                <div style="margin-bottom: 1rem;">
                    <p style="margin: 0; color: #adb5bd; font-weight: 500;">Bins Collected: <strong style="color: #89d957;">34</strong></p>
                    <div style="background: #495057; height: 10px; border-radius: 5px; margin-top: 0.5rem;">
                        <div style="background: linear-gradient(90deg, #89d957, #81865e); width: 68%; height: 100%; border-radius: 5px;"></div>
                    </div>
                </div>
                <div style="margin-bottom: 1rem;">
                    <p style="margin: 0; color: #adb5bd; font-weight: 500;">Recycled Items: <strong style="color: #89d957;">156</strong></p>
                    <div style="background: #495057; height: 10px; border-radius: 5px; margin-top: 0.5rem;">
                        <div style="background: linear-gradient(90deg, #89d957, #81865e); width: 78%; height: 100%; border-radius: 5px;"></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Eco Impact Card
        st.markdown("""
            <div class="card" style="padding: 2rem;">
                <h4 style="color: #81865e; margin-bottom: 1rem;">🌱 Eco Impact</h4>
                <img src="https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=300&h=150&fit=crop&crop=center" 
                     style="width: 100%; height: 120px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem;">
                <p style="color: #636e72; font-size: 0.9rem; line-height: 1.5;">CO₂ saved this month: <strong style="color: #89d957;">2.4 tons</strong></p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="card" style="padding: 2rem;">
                <h3 style="color: #81865e; margin-bottom: 1.5rem;">📍 Smart Bin Monitoring</h3>
                <img src="https://plus.unsplash.com/premium_photo-1663050693144-6b5bc76d2214?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" 
                style="width: 100%; height: 180px; object-fit: cover; border-radius: 12px; margin-bottom: 1rem;">
                <p style="color: #636e72; line-height: 1.6;">Real-time monitoring of bin fill levels across the city with predictive analytics for optimal collection routes.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card" style="padding: 2rem;">
                <h3 style="color: #81865e; margin-bottom: 1.5rem;">♻️ Sustainability Goals</h3>
                <img src="https://plus.unsplash.com/premium_photo-1679607581922-ba5c2558669b?q=80&w=715&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" 
                     style="width: 100%; height: 180px; object-fit: cover; border-radius: 12px; margin-bottom: 1rem;">
                <p style="color: #636e72; line-height: 1.6;">Track progress towards zero waste goals and promote sustainable practices in your community.</p>
            </div>
        """, unsafe_allow_html=True)

# --- Trash Classification ---
    
if page == "Trash Classification":
    st.header("🗑️ Trash Classification")
    st.markdown("<p style='text-align:center; color:#636e72; font-size: 1.1rem;'>Upload an image of a waste item for AI classification.</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload an image of trash", type=['png','jpg','jpeg'])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Trash Image", use_container_width=True)

        if st.button("Classify Trash"):
            with st.spinner('AI is classifying the trash...'):
                try:
                    # Send file to Flask backend
                    files = {"file": uploaded_file.getvalue()}
                    response = requests.post("http://127.0.0.1:5000/classify", files=files)

                    if response.status_code == 200:
                        result = response.json()
                        predicted_class = result.get("class", "Unknown")
                        
                        st.markdown(f"""
                            <div class="result-card">
                                <h3 style="color: #f8f9fa;">Prediction Result</h3>
                                <p style="font-size: 1.2rem; color: #adb5bd;"><strong>Class:</strong> <span style="color: #89d957; font-weight: 700;">{predicted_class.upper()}</span></p>
                            </div>
                        """, unsafe_allow_html=True)

                        # Contextual Info
                        if predicted_class.lower() in ["cardboard", "paper"]:
                            st.info("This item is recyclable! ♻️")
                        elif predicted_class.lower() in ["metal", "glass"]:
                            st.info("This material can be recycled efficiently. 🔄")
                        elif predicted_class.lower() == "plastic":
                            st.warning("Plastic detected. Consider recycling responsibly. 🚯")
                        else:
                            st.error("This is general waste. 🚮")
                    else:
                        st.error(f"Error from Flask server: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Flask server not running.")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")

# --- Bin Fill Prediction ---
if page == "Bin Fill Prediction":
    # Page Header with Image
    st.markdown("""
        <div style="position: relative; background: linear-gradient(135deg, rgba(137, 217, 87, 0.9), rgba(129, 134, 94, 0.9)), url('https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200&h=300&fit=crop&crop=center'); background-size: cover; background-position: center; padding: 3rem 2rem; border-radius: 20px; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700;">📊 Smart Bin Monitoring</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">Real-time fill level tracking and predictive analytics</p>
        </div>
    """, unsafe_allow_html=True)
    
    bins_data = {
        "Bin A": {"fill_level": 75, "prediction": 90, "location": "Central Park", "status": "Normal"},
        "Bin B": {"fill_level": 40, "prediction": 55, "location": "Main Street", "status": "Normal"},
        "Bin C": {"fill_level": 95, "prediction": 98, "location": "Shopping Mall", "status": "Critical"}
    }
    df = pd.DataFrame(bins_data).T
    df.index.name = "Bin"

    st.markdown("### Current & Predicted Fill Levels")
    col1, col2, col3 = st.columns(3)
    
    bin_images = [
        "https://images.unsplash.com/photo-1697142351891-a52168fcbd4e?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=300&h=200&fit=crop&crop=center",
        "https://images.unsplash.com/photo-1699108872796-348069f97608?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    ]
    
    for idx, bin_name in enumerate(df.index):
        with [col1, col2, col3][idx]:
            fill_level = df.loc[bin_name,'fill_level']
            prediction = df.loc[bin_name,'prediction']
            location = df.loc[bin_name,'location']
            status = df.loc[bin_name,'status']
            
            status_color = "#e74c3c" if status == "Critical" else "#89d957"
            
            st.markdown(f"""
                <div class="card" style="padding: 1.5rem;">
                    <img src="{bin_images[idx]}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem;">
                    <h3 style="color: #81865e; margin: 0 0 0.5rem 0;">{bin_name}</h3>
                    <p style="color: #636e72; margin: 0 0 1rem 0; font-size: 0.9rem;">📍 {location}</p>
                    <div style="margin-bottom: 1rem;">
                        <p style="margin: 0 0 0.5rem 0; color: #636e72;">Current: <strong style="color: #81865e;">{fill_level}%</strong></p>
                        <div style="background: #e8f4e8; height: 8px; border-radius: 4px;">
                            <div style="background: linear-gradient(90deg, #89d957, #81865e); width: {fill_level}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <p style="margin: 0 0 0.5rem 0; color: #636e72;">Predicted: <strong style="color: #89d957;">{prediction}%</strong></p>
                        <div style="background: #e8f4e8; height: 8px; border-radius: 4px;">
                            <div style="background: linear-gradient(90deg, #81865e, #89d957); width: {prediction}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </div>
                    <p style="margin: 0; color: {status_color}; font-weight: 600; font-size: 0.9rem;">● {status}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <div class="card" style="padding: 2rem;">
                <h3 style="color: #81865e; margin-bottom: 1.5rem;">📈 Fill Level Trends</h3>
        """, unsafe_allow_html=True)
        
        chart_data = pd.DataFrame({
            "time": range(10),
            "Bin A": [10, 15, 20, 30, 45, 60, 70, 75, 80, 85],
            "Bin B": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
            "Bin C": [2, 5, 10, 15, 25, 35, 50, 60, 75, 95]
        })
        st.line_chart(chart_data.set_index('time'))
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card" style="padding: 2rem;">
                <h3 style="color: #81865e; margin-bottom: 1.5rem;">📋 Quick Actions</h3>
                <img src="https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=300&h=150&fit=crop&crop=center" 
                     style="width: 100%; height: 120px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem;">
        """, unsafe_allow_html=True)
        
        csv = df.to_csv().encode('utf-8')
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom section with download button
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Fetch Live Predictions", key="fetch_live"):
            st.info("Fetching live predictions...")
    
    with col2:
        csv = df.to_csv().encode('utf-8')
        st.download_button(
        label="Download Prediction Data as CSV",
            data=csv,
            file_name='bin_fill_predictions.csv',
            mime='text/csv',
            key='bin_fill_download_bottom',
            help="Download bin fill prediction data as CSV"
        )

    # Live predictions logic (removed session state dependency for now)
    # This will be handled by the button click above

# --- Sustainable Tips ---
if page == "Sustainable Tips":
    st.header("💡 Sustainable Living Tips")
    
    tips_with_images = {
        "Compost": {
            "text": "Start a compost bin for your food scraps.",
            "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=200&fit=crop&crop=center"
        },
        "Reusable Bags": {
            "text": "Bring your own reusable bags when shopping.",
            "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=200&fit=crop&crop=center"
        },
        "Repair, Don't Replace": {
            "text": "Try to fix broken items first.",
            "image": "https://plus.unsplash.com/premium_photo-1737180621286-c2250ccce178?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        "Reduce Paper": {
            "text": "Go paperless whenever possible.",
            "image": "https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=400&h=200&fit=crop&crop=center"
        },
        "Mindful Consumption": {
            "text": "Buy only what you need.",
            "image": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=400&h=200&fit=crop&crop=center"
        }
    }
    
    # Create columns for better alignment
    col1, col2 = st.columns(2)
    
    tips_list = list(tips_with_images.items())
    
    # First column - first 3 tips
    with col1:
        for i in range(0, len(tips_list), 2):
            if i < len(tips_list):
                title, content = tips_list[i]
                st.markdown(f"""
                <div class="card" style="margin-bottom: 1.5rem; padding: 1.5rem; min-height: 280px; max-height: 280px;">
                    <img src="{content['image']}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem;">
                    <h3 style="color: #f8f9fa; margin-bottom: 0.8rem; font-size: 1.1rem;">{title}</h3>
                    <p style="color: #adb5bd; line-height: 1.4; font-size: 0.9rem;">{content['text']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Second column - remaining tips
    with col2:
        for i in range(1, len(tips_list), 2):
            if i < len(tips_list):
                title, content = tips_list[i]
                st.markdown(f"""
                <div class="card" style="margin-bottom: 1.5rem; padding: 1.5rem; min-height: 280px; max-height: 280px;">
                    <img src="{content['image']}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem;">
                    <h3 style="color: #f8f9fa; margin-bottom: 0.8rem; font-size: 1.1rem;">{title}</h3>
                    <p style="color: #adb5bd; line-height: 1.4; font-size: 0.9rem;">{content['text']}</p>
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
    st.markdown("<p style='text-align:center; color:#636e72; font-size: 1.1rem;'>We aim to revolutionize waste collection with a sustainable future in mind.</p>", unsafe_allow_html=True)
    st.subheader("Meet the Team")
    col1, col2 = st.columns(2)
    team = [("Anshika Singh","AI/ML & Web Developer"), ("Shreya Sharma","Frontend Developer")]
    for col, (name,role) in zip([col1,col2], team):
        with col:
            st.markdown(f"<div class='card'><h3>{name}</h3><p>{role}</p></div>", unsafe_allow_html=True)
