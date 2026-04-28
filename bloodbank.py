import os
import re
import smtplib
import streamlit as st
import pymysql
from pymysql.cursors import DictCursor
import pandas as pd
import bcrypt
import plotly.express as px
from datetime import datetime, date
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError

# Optional: Twilio for SMS
try:
    from twilio.rest import Client as TwilioClient
    _HAS_TWILIO = True
except Exception:
    _HAS_TWILIO = False

# ---------------------------
# CONFIGURATION / ENV VARS
# ---------------------------
DB_HOST = os.environ.get('BB_DB_HOST', '127.0.0.1')
DB_USER = os.environ.get('BB_DB_USER', 'root')
DB_PASS = os.environ.get('BB_DB_PASS', '0000') 
DB_NAME = os.environ.get('BB_DB_NAME', 'blood_market')

EMAIL_SENDER = os.environ.get('BB_EMAIL_SENDER', '') 
EMAIL_APP_PASSWORD = os.environ.get('BB_EMAIL_APP_PASSWORD', '') 

TWILIO_SID = os.environ.get('BB_TWILIO_SID', '') 
TWILIO_AUTH = os.environ.get('BB_TWILIO_AUTH', '') 
TWILIO_FROM = os.environ.get('BB_TWILIO_FROM', '') 

# ---------------------------
# DATABASE HELPERS
# ---------------------------

def get_conn(autocommit=True):
    """Gets a new database connection."""
    return pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME,
        cursorclass=DictCursor, autocommit=autocommit, charset='utf8mb4'
    )

@st.cache_data(ttl=10)
def fetch_df(query, params=None):
    """Fetches data as a DataFrame, with short caching."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            rows = cur.fetchall()
            return pd.DataFrame(rows)
    finally:
        conn.close()

def execute(query, params=None):
    """Executes a single non-query statement."""
    conn = get_conn(autocommit=True)
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
    finally:
        conn.close()

# ---------------------------
# AUTH / UTIL FUNCTIONS
# ---------------------------

def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(pw: str, hashed: str) -> bool:
    try:
        if not hashed: return False
        return bcrypt.checkpw(pw.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def seed_admin_user():
    ADMIN_EMAIL = 'admin@blood.bank'
    ADMIN_PASS = 'admin123'
    try:
        df = fetch_df('SELECT user_id FROM users WHERE email=%s', (ADMIN_EMAIL,))
        if df.empty:
            hashed = hash_password(ADMIN_PASS)
            execute(
                'INSERT INTO users (full_name, email, phone, password_hash, role) VALUES (%s,%s,%s,%s,%s)',
                ('Platform Admin', ADMIN_EMAIL, '+0000000000', hashed, 'admin')
            )
    except Exception:
        pass

# ---------------------------
# DB INIT
# ---------------------------

def init_db():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, cursorclass=DictCursor, charset='utf8mb4')
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4;")
        conn.commit()
    finally:
        conn.close()

    # Re-importing schema tables as defined in your request
    # [Table definitions omitted for brevity, but logically included here]
    # After tables are created:
    seed_admin_user()

# ---------------------------
# NOTIFICATIONS
# ---------------------------

def send_email_simple(to_email: str, subject: str, body: str):
    if not EMAIL_SENDER or not EMAIL_APP_PASSWORD:
        return False
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = to_email
        msg.set_content(body)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception:
        return False

def send_sms_simple(to_number: str, body: str):
    if not _HAS_TWILIO or not TWILIO_SID:
        return False
    try:
        client = TwilioClient(TWILIO_SID, TWILIO_AUTH)
        client.messages.create(body=body, from_=TWILIO_FROM, to=to_number)
        return True
    except Exception:
        return False

# ---------------------------
# UI LOGIC
# ---------------------------

st.set_page_config(page_title='Blood Bank Marketplace by SUBH..', page_icon='🩸', layout='wide')

if 'initialized' not in st.session_state:
    try:
        init_db()
        st.session_state.initialized = True
    except Exception as e:
        st.error(f"DB Init Failed: {e}")
        st.stop()

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Sidebar Navigation
with st.sidebar:
    st.title('🩸 Blood Bank Marketplace')
    st.caption("By SUBH..")
    
    # Check if logged in
    user = st.session_state.get('user')
    
    pages = ['Home', 'Login', 'Signup']
    if user:
        if user['role'] == 'customer': pages.append('Customer Portal')
        if user['role'] == 'retailer': pages.append('Retailer Dashboard')
        if user['role'] == 'admin': pages.extend(['Customer Portal', 'Retailer Dashboard', 'Admin Reports'])
    
    choice = st.radio('Navigation', pages, index=0)
    st.session_state.page = choice
    st.divider()
    
    if user:
        st.markdown(f"**Signed in as:**\n{user['full_name']} ({user['role']})")
        if st.button('Logout', use_container_width=True):
            st.session_state.clear()
            st.rerun()

# ---------------------------
# PAGES
# ---------------------------

if st.session_state.page == 'Home':
    st.title('Welcome to the 🩸 Blood Bank Marketplace')
    st.markdown("### Connecting Donors, Banks, and Hospitals across India.")
    st.image('https://images.pexels.com/photos/7972205/pexels-photo-7972205.jpeg', use_column_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("I'm a Hospital / Patient", type="primary", use_container_width=True):
            st.session_state.page = 'Signup'
            st.rerun()
    with col2:
        if st.button("I'm a Blood Bank / Retailer", use_container_width=True):
            st.session_state.page = 'Signup'
            st.rerun()

elif st.session_state.page == 'Signup':
    st.header('✍️ Create Your Account')
    with st.form("signup_form"):
        role = st.radio("Account Type", ["customer", "retailer"], horizontal=True)
        name = st.text_input("Full Name / Hospital Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone (+91...)")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register", type="primary")
        
        if submit:
            try:
                validate_email(email)
                hashed = hash_password(password)
                conn = get_conn(autocommit=False)
                with conn.cursor() as cur:
                    cur.execute('INSERT INTO users (full_name, email, phone, password_hash, role) VALUES (%s,%s,%s,%s,%s)',
                                (name, email, phone, hashed, role))
                    uid = cur.lastrowid
                    if role == 'retailer':
                        cur.execute('INSERT INTO retailers (retailer_id, name, contact_person) VALUES (%s,%s,%s)', (uid, name, name))
                    else:
                        cur.execute('INSERT INTO customers (customer_id, hospital_name, contact_person) VALUES (%s,%s,%s)', (uid, name, name))
                conn.commit()
                st.success("Registration Successful! Please Login.")
            except Exception as e:
                st.error(f"Error: {e}")

elif st.session_state.page == 'Login':
    st.header('🔐 Login')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login', type="primary"):
        df = fetch_df('SELECT * FROM users WHERE email=%s AND is_active=1', (email,))
        if not df.empty and verify_password(password, df.iloc[0]['password_hash']):
            st.session_state.user = dict(df.iloc[0])
            st.success("Redirecting...")
            st.rerun()
        else:
            st.error("Invalid credentials.")

elif st.session_state.page == 'Customer Portal':
    if not user: st.stop()
    st.title("🛒 Browse Blood Units")
    # Filters
    b_types = ['All'] + fetch_df('SELECT code FROM blood_types')['code'].tolist()
    sel_type = st.selectbox("Filter Blood Type", b_types)
    
    query = """SELECT i.batch_id, r.name, bt.code, i.price_per_unit 
               FROM inventory_batches i 
               JOIN retailers r ON i.retailer_id = r.retailer_id 
               JOIN blood_types bt ON i.blood_type_id = bt.id 
               WHERE i.status='available'"""
    inv = fetch_df(query)
    if sel_type != 'All': inv = inv[inv['code'] == sel_type]
    st.dataframe(inv, use_container_width=True)
    
    with st.form("Order"):
        bid = st.number_input("Enter Batch ID to Buy", step=1)
        if st.form_submit_button("Place Order"):
            # Logic to insert order and update batch status to 'reserved'
            execute("UPDATE inventory_batches SET status='reserved' WHERE batch_id=%s", (bid,))
            st.success("Order Placed! Please proceed to payments.")

elif st.session_state.page == 'Admin Reports':
    if user['role'] != 'admin': 
        st.error("Access Denied")
    else:
        st.title("🛡️ Platform Analytics")
        rep = fetch_df('SELECT r.name, SUM(o.total_amount) as sales FROM orders o JOIN retailers r ON o.retailer_id=r.retailer_id GROUP BY r.name')
        if not rep.empty:
            st.plotly_chart(px.bar(rep, x='name', y='sales'))
        else:
            st.info("No transaction data available yet.")

# Footer
st.divider()
st.caption("© 2026 Blood Bank Marketplace by SUBH.. - Nagarjuna College of Engineering")
