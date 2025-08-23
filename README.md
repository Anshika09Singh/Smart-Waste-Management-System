# ♻️ Smart Waste Management System

A **Smart Waste Management System** powered by **AI/ML** to **classify trash automatically** and **predict bin fill levels** for optimized waste collection.  
This project aims to **reduce carbon footprint**, **encourage recycling**, and **improve urban waste management**.  

---

## 📝 Table of Contents  

- [About](#about)  
- [Features](#features)  
- [Technologies Used](#technologies-used)  
- [Dataset](#dataset)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Contributing](#contributing)  
- [License](#license)  

---

## 📌 About  

This project integrates **computer vision** and **predictive analytics** for efficient waste management.  
It uses a **CNN model** to classify trash into categories and a **bin fill prediction model** to forecast collection needs.  

**Objectives:**  
- Classify waste images into predefined categories.  
- Predict bin fill levels for optimized collection routes.  
- Provide an interactive and user-friendly frontend.  
- Promote sustainable and eco-friendly waste practices.  

---

## ✨ Features  

- **Trash Classification**: Upload waste images, AI predicts category (cardboard, glass, metal, paper, plastic, trash).  
- **Bin Fill Prediction**: Forecasts bin fill levels for the next 24 hours.  
- **Interactive Frontend**: Built with Streamlit for easy navigation.  
- **Data Export**: Download prediction results as `.csv`.  
- **Cross-Platform**: Works on desktop and mobile browsers.  

---

## 🛠 Technologies Used  

- **Frontend**: Streamlit, HTML/CSS, Requests, PIL  
- **Backend**: Flask, Flask-CORS  
- **Machine Learning**: TensorFlow/Keras (CNN for classification), RandomForestRegressor (for prediction)  
- **Data Processing**: Pandas, NumPy  
- **Visualization**: Streamlit Charts  

---

## 📂 Dataset  

- **Trash Classification Dataset**: [TrashNet (Kaggle)](https://www.kaggle.com/datasets/asdasdasd/trashnet)  
  Contains labeled images for:  
  - Cardboard  
  - Glass  
  - Metal  
  - Paper  
  - Plastic  
  - Trash  

- **Bin Fill Simulation Dataset**:  
  A synthetic dataset is generated for bin fill levels recorded hourly across bins (`bin1`, `bin2`, etc.).  

---

## 💻 Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/smart-waste-management.git
   cd smart-waste-management

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python app.py
streamlit run streamlit_demo.py

🚀 Usage

Open the Streamlit app in the browser.

Go to Trash Classification → upload an image → view predicted category.

Go to Bin Fill Prediction → view forecasted fill levels for bins.

Export results as CSV if needed.
