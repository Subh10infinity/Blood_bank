# 🩸 Blood Bank Marketplace

A full-stack web application built with **Python, Streamlit, and MySQL** to create a real-time marketplace connecting blood banks (Retailers) and hospitals (Customers). This project provides a complete portal for inventory management, order processing, and platform-wide analytics.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

---

## ✨ Key Features

This platform is built with three distinct user roles, each with a dedicated portal:

### 🏥 Customer (Hospital) Portal
* **Browse Inventory:** Search and filter available blood units by blood type, city, and price.
* **Place Orders:** Securely place orders for specific blood batches.
* **Payment Simulation:** A complete order-to-payment workflow (simulated).
* **Order History:** View and track the status of all past and current orders.

### 🏦 Retailer (Blood Bank) Dashboard
* **Sales Analytics:** View interactive charts (built with Plotly) for sales over time, sales by blood type, and average ratings.
* **Inventory Management:** Add new blood batches (from donations or external procurement) and manage existing stock.
* **Donation Management:** A complete module to register new donors and record donations, which automatically links to the inventory.
* **Order Management:** View and update the status of incoming orders (e.g., 'Confirmed', 'Shipped', 'Delivered').

### 🛡️ Admin Reports
* **Platform Oversight:** A high-level dashboard to monitor sales performance across all retailers.
* **User Management:** (Via `seed_admin_user` function for initial setup).
* **Top Donors:** View a platform-wide report of top donors.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit (for the entire web interface)
* **Backend:** Python
* **Database:** MySQL
* **Database Connector:** `pymysql`
* **Data Manipulation:** `pandas`
* **Visualization:** `plotly.express`
* **Security:** `bcrypt` (for password hashing and verification)
* **Utilities:** `email_validator`, `smtplib` (for email notifications), `twilio` (for SMS notifications)

---

## 🚀 Getting Started

Follow these steps to get a local copy of the project up and running.

### Prerequisites

* Python 3.8+
* A running MySQL server (e.g., XAMPP, WAMP, or MySQL Community Server)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

### 2. Install Dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the required packages:
```bash
pip install streamlit pymysql pandas bcrypt email_validator plotly twilio
```

### 3. Set Up the Database

1.  Open your MySQL command-line or admin tool (like phpMyAdmin).
2.  Create a new database. The app defaults to `blood_market`, but you can use any name.
    ```sql
    CREATE DATABASE blood_market;
    ```
3.  **No need to create tables manually!** The `init_db()` function in the app will create all the tables for you on the first run.

### 4. Configure Environment Variables

This project uses Streamlit's built-in secrets management.

1.  Create a folder in your project directory: `.streamlit`
2.  Inside that folder, create a file: `secrets.toml`
3.  Add your credentials to this file:

```toml
# .streamlit/secrets.toml

# MySQL Database
BB_DB_HOST = "127.0.0.1"
BB_DB_USER = "root"
BB_DB_PASS = "YOUR_MYSQL_PASSWORD"  # e.g., "0000"
BB_DB_NAME = "blood_market"

# Optional: Email (Gmail)
BB_EMAIL_SENDER = "your-email@gmail.com"
BB_EMAIL_APP_PASSWORD = "your-16-digit-app-password"

# Optional: Twilio SMS
BB_TWILIO_SID = "YOUR_TWILIO_SID"
BB_TWILIO_AUTH = "YOUR_TWILIO_AUTH_TOKEN"
BB_TWILIO_FROM = "+1234567890"
```

### 5. Run the Application

Once your `secrets.toml` is saved, run the app from your terminal:

```bash
streamlit run app.py
```

The app will open in your browser. The database and admin user will be seeded on the first run.

---

## 🧑‍💻 How to Use

1.  **Admin:**
    * **Email:** `admin@blood.bank`
    * **Password:** `admin123`
    * Navigate to the **Admin Reports** page to see platform-wide data.

2.  **Retailer (Blood Bank):**
    * Go to the **Signup** page.
    * Select "Blood Bank (Retailer)" and create an account.
    * Log in and use the **Retailer Dashboard** to add inventory and manage sales.

3.  **Customer (Hospital):**
    * Go to the **Signup** page.
    * Select "Hospital (Customer)" and create an account.
    * Log in and use the **Customer Portal** to browse and order blood.

---

## 📸 Screenshots

*(Recommended: Add 3-4 screenshots of your app here!)*

| Login Page | Retailer Dashboard | Customer Portal |
| :---: | :---: | :---: |
| 

[Image of Login]
 |  |  |
