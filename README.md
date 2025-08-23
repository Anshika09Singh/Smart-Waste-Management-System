# ♻️ Smart Waste Management System

A **Smart Waste Management System** powered by AI/ML to **classify trash automatically** and **predict bin fill levels** for optimized waste collection. This project aims to reduce carbon footprint, encourage recycling, and improve urban waste management.

---

## 📝 Table of Contents

- [About](#about)  
- [Features](#features)  
- [Technologies Used](#technologies-used)  
- [Dataset](#dataset)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Screenshots](#screenshots)  
- [Contributing](#contributing)  
- [License](#license)  

---

## 📌 About

This AI-powered system uses **image recognition** to classify trash into categories and **predictive modeling** to forecast bin fill levels. The system consists of a **Flask backend** for ML inference and a **Streamlit frontend** for interactive user experience.

**Key Objectives:**

- Automatically classify trash into categories.  
- Predict bin fill levels for efficient waste collection.  
- Provide visual insights using interactive charts.  
- Make waste management smarter and eco-friendly.  

---

## ✨ Features

1. **Trash Classification**  
   - Upload images of trash (png, jpg, jpeg).  
   - AI model predicts the category: `cardboard`, `glass`, `metal`, `paper`, `plastic`, `trash`.  

2. **Bin Fill Prediction**  
   - Predict fill levels of bins for next hours.  
   - Interactive charts and progress bars.  

3. **User-friendly Frontend**  
   - Streamlit app with light theme, modern fonts, hover effects, and animations.  
   - Navigation tabs for Home, Trash Classification, and Bin Fill Prediction.  

4. **Data Download**  
   - Export predicted fill levels as CSV.  

5. **Responsive Design**  
   - Works on desktop and mobile devices.  

---

## 🛠 Technologies Used

- **Frontend:** Streamlit, HTML/CSS, PIL, requests  
- **Backend:** Flask, Flask-CORS  
- **Machine Learning:** TensorFlow/Keras, RandomForestRegressor  
- **Data Processing:** Pandas, NumPy  
- **Visualization:** Streamlit charts  

---

## 📂 Dataset

**Trash Classification:**  
- **TrashNet Dataset (Kaggle):** [https://www.kaggle.com/datasets/asdasdasd/trashnet](https://www.kaggle.com/datasets/asdasdasd/trashnet)  

**Bin Fill Simulation:**  
- Simulated dataset using hourly bin fill percentages for multiple bins (`bin1`, `bin2`).  

**Categories Used:**  
- Cardboard  
- Glass  
- Metal  
- Paper  
- Plastic  
- Trash  

**Example Images:**  
- Cardboard: ![Cardboard](https://images.unsplash.com/photo-1581091215364-6f5398f04943?auto=format&fit=crop&w=600&q=80)  
- Glass: ![Glass](https://images.unsplash.com/photo-1602524207562-1f257f87a7c1?auto=format&fit=crop&w=600&q=80)  
- Plastic: ![Plastic](https://images.unsplash.com/photo-1584302171419-859d6f80bfb0?auto=format&fit=crop&w=600&q=80)  

*(Add more example images if needed.)*

---

## 💻 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/smart-waste-management.git
cd smart-waste-management

python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt

python app.py

streamlit run streamlit_demo.py
