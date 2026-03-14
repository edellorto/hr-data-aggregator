"""
HR & RECRUITING DATA AGGREGATOR - STREAMLIT APP
Versione semplificata per Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============================================================================

# PAGE CONFIG

# ============================================================================

st.set_page_config(
    page_title="HR & Recruiting Data Hub",
    page_icon="📊",
    layout="wide"
)

# ============================================================================

# SESSION STATE

# ============================================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.user_role = None

# ============================================================================

# DEMO DATA

# ============================================================================

@st.cache_data
def generate_demo_data():
    """Genera dati di demo"""
    
    np.random.seed(42)
    
    
# Workforce data

    employees = {
        'employee_id': [f'EMP_{i:05d}' for i in range(1, 101)],
        'first_name': np.random.choice(['John', 'Jane', 'Bob', 'Alice', 'Charlie'], 100),
        'last_name': np.random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'], 100),
        'email': [f'emp_{i:05d}@deloitte.com' for i in range(1, 101)],
        'role': np.random.choice(['Consultant', 'Senior Consultant', 'Manager'], 100),
        'service_line': np.random.choice(['Consulting', 'Financial Advisory', 'Technology'], 100),
        'location': np.random.choice(['Italy', 'Europe'], 100),
        'gender': np.random.choice(['Male', 'Female'], 100),
        'age': np.random.randint(25, 60, 100),
    }
    
    workforce_df = pd.DataFrame(employees)
    
    
# Recruiting data

    candidates = {
        'candidate_id': [f'CAN_{i:05d}' for i in range(1, 51)],
        'first_name': np.random.choice(['John', 'Jane', 'Bob', 'Alice', 'Charlie'], 50),
        'last_name': np.random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'], 50),
        'position': np.random.choice(['Consultant', 'Senior Consultant', 'Manager'], 50),
        'service_line': np.random.choice(['Consulting', 'Financial Advisory', 'Technology'], 50),
        'status': np.random.choice(['Pipeline', 'Interview', 'Offer', 'Hired'], 50),
        'gender': np.random.choice(['Male', 'Female'], 50),
    }
    
    recruiting_df = pd.DataFrame(candidates)
    
    return workforce_df, recruiting_df

# ============================================================================

# LOGIN PAGE

# ============================================================================

def show_login_page():
    """Mostra la pagina di login"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🔐 HR & Recruiting Data Hub")
        st.markdown("---")
        
        st.markdown("
### Login")

        
        user_id = st.text_input("User ID", placeholder="e.g., REC_001")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            demo_users = {
                "REC_001": {"password": "test123", "name": "John Recruiter", "role": "recruiter"},
                "REC_MGR_001": {"password": "test123", "name": "Jane Manager", "role": "manager"},
                "HRBP_001": {"password": "test123", "name": "Bob HRBP", "role": "hrbp"},
            }
            
            if user_id in demo_users and demo_users[user_id]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.user = demo_users[user_id]["name"]
                st.session_state.user_role = demo_users[user_id]["role"]
                st.success(f"Welcome, {st.session_state.user}!")
                st.rerun()
            else:
                st.error("Invalid credentials")
        
        st.markdown("---")
        st.markdown("""
        **Demo Credentials:**
        - REC_001 / test123
        - REC_MGR_001 / test123
        - HRBP_001 / test123
        """)

# ============================================================================

# MAIN APP

# ============================================================================

def show_main_app():
    """Mostra l'applicazione principale"""
    
    workforce_df, recruiting_df = generate_demo_data()
    
    
# Sidebar

    with st.sidebar:
        st.title("🎯 HR Data Hub")
        st.markdown(f"**User:** {st.session_state.user}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "👥 Workforce", "🎯 Recruiting", "📋 Data Quality"]
        )
        
        st.markdown("---")
        
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    
# Pages

    if page == "📊 Dashboard":
        st.title("📊 Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Headcount", len(workforce_df))
        with col2:
            st.metric("🎯 Pipeline", len(recruiting_df))
        with col3:
            hired = len(recruiting_df[recruiting_df['status'] == 'Hired'])
            st.metric("✅ Hired", hired)
        with col4:
            st.metric("📊 Sources", 2)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Headcount by Service Line")
            sl_counts = workforce_df['service_line'].value_counts()
            st.bar_chart(sl_counts)
        
        with col2:
            st.subheader("Candidate Status")
            status_counts = recruiting_df['status'].value_counts()
            st.bar_chart(status_counts)
    
    elif page == "👥 Workforce":
        st.title("👥 Workforce")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", len(workforce_df))
        with col2:
            male = len(workforce_df[workforce_df['gender'] == 'Male'])
            st.metric("Male", male)
        with col3:
            female = len(workforce_df[workforce_df['gender'] == 'Female'])
            st.metric("Female", female)
        
        st.markdown("---")
        st.subheader("Workforce Data")
        st.dataframe(workforce_df, use_container_width=True)
    
    elif page == "🎯 Recruiting":
        st.title("🎯 Recruiting")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", len(recruiting_df))
        with col2:
            hired = len(recruiting_df[recruiting_df['status'] == 'Hired'])
            st.metric("Hired", hired)
        with col3:
            pipeline = len(recruiting_df[recruiting_df['status'] == 'Pipeline'])
            st.metric("Pipeline", pipeline)
        with col4:
            interview = len(recruiting_df[recruiting_df['status'] == 'Interview'])
            st.metric("Interview", interview)
        
        st.markdown("---")
        st.subheader("Candidate Data")
        st.dataframe(recruiting_df, use_container_width=True)
    
    elif page == "📋 Data Quality":
        st.title("📋 Data Quality")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Workforce Records", len(workforce_df))
        with col2:
            st.metric("Recruiting Records", len(recruiting_df))
        with col3:
            st.metric("Total", len(workforce_df) + len(recruiting_df))
        
        st.markdown("---")
        st.info("✅ All data sources are fresh and up-to-date")

# ============================================================================

# MAIN

# ============================================================================

def main():
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
