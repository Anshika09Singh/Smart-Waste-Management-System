# ♻️ Smart Waste Management System

An **AI/ML-powered Smart Waste Management System** that **automatically classifies trash** and **predicts bin fill levels** for optimized, efficient, and sustainable waste collection. This project is a step toward a greener future, aiming to **reduce carbon footprint**, **encourage recycling**, and **modernize urban waste management**.

---

## ✨ A Glimpse into the Future of Waste Management

Waste management is a critical challenge for modern cities, with inefficient collection methods leading to high operational costs and environmental damage. Our Smart Waste Management System tackles this head-on by leveraging the power of **Artificial Intelligence** and **Machine Learning**. It moves beyond traditional, time-based collection schedules to a proactive, data-driven approach.

By automatically classifying waste, we can make recycling smarter and more accessible for everyone. The system's ability to predict when bins will be full allows for more efficient collection routes, which in turn reduces fuel consumption and minimizes the carbon footprint of waste vehicles. Imagine a city where waste collection is a seamless, data-driven process, ensuring cleaner streets and a healthier planet. This project is a step toward that sustainable future.



---

## 📌 About

This project seamlessly integrates **computer vision** and **predictive analytics** to create an efficient waste management solution. It uses a sophisticated **Convolutional Neural Network (CNN)** model to classify trash and a **predictive model** to forecast bin collection needs.

**Our Core Objectives:**

-   **Classify Waste Images:** Accurately sort waste into predefined categories.
-   **Optimize Collection Routes:** Predict bin fill levels to create cost-effective and energy-saving collection schedules.
-   **Provide an Intuitive Interface:** Offer a user-friendly and interactive web application for easy use.
-   **Promote Sustainability:** Encourage and facilitate eco-friendly waste disposal practices.

---

## ✨ Key Features

-   **Automated Trash Classification:** Simply upload a waste image, and the AI will instantly predict its category (cardboard, glass, metal, paper, plastic, or trash).
-   **Predictive Bin-Level Forecasting:** Our system forecasts bin fill levels for the next 24 hours, enabling proactive and on-demand collection.
-   **Interactive Dashboard:** A clean, easy-to-use interface built with **Streamlit** for seamless navigation and data visualization.
-   **Data Export Functionality:** Easily download prediction results and data in a convenient **.csv** format for further analysis.
-   **Cross-Platform Compatibility:** The web application is fully responsive and works flawlessly on desktop and mobile browsers.

---

## 🛠 Technologies & Tools

| Category            | Technologies                                          |
| :------------------ | :---------------------------------------------------- |
| **Frontend** | Streamlit, HTML/CSS, Requests, PIL                    |
| **Backend** | Flask, Flask-CORS                                     |
| **Machine Learning**| TensorFlow/Keras (CNN), RandomForestRegressor         |
| **Data Processing** | Pandas, NumPy                                         |
| **Visualization** | Streamlit Charts                                      |

---

## 📂 Dataset

### Trash Classification Dataset

We used the **TrashNet dataset** from [Kaggle]([https://www.kaggle.com/datasets/asdasdasd/trashnet](https://www.kaggle.com/datasets/feyzazkefe/trashnet)), which contains labeled images for six waste categories:
-   Cardboard
-   Glass
-   Metal
-   Paper
-   Plastic
-   Trash

### Bin Fill Simulation Dataset

A synthetic dataset was generated to simulate hourly bin fill levels across various bins (`bin1`, `bin2`, etc.), which was used to train our predictive model.

---

## 💻 Installation

Get a copy of the project up and running on your local machine with these simple steps.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/smart-waste-management.git](https://github.com/yourusername/smart-waste-management.git)
    cd smart-waste-management
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    ```
    -   **On Linux/Mac:**
        ```bash
        source venv/bin/activate
        ```
    -   **On Windows:**
        ```bash
        venv\Scripts\activate
        ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    # Start the backend Flask server
    python app.py
    
    # In a new terminal, start the Streamlit frontend
    streamlit run streamlit_demo.py
    ```
    
---

## 🚀 Usage

1.  Open the Streamlit app in your web browser.
2.  Navigate to the **Trash Classification** tab, upload an image, and see the AI's prediction.
3.  Go to the **Bin Fill Prediction** tab to view the forecasted fill levels for your bins.
4.  Download the results in CSV format if needed.





---

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.
