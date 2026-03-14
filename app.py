"""
HR & RECRUITING DATA AGGREGATOR - MAIN APPLICATION
====================================================

Applicazione Streamlit per Google Cloud Run

Esecuzione:
  streamlit run app.py

CLASSIFICAZIONE: Internal Use Only - Deloitte
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
import os
from pathlib import Path

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="HR & Recruiting Data Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.user_role = None

# ============================================================================
# DEMO DATA GENERATOR
# ============================================================================

@st.cache_data
def generate_demo_data():
    """Genera dati di demo per il testing"""
    
    np.random.seed(42)
    
    # Workforce data
    employees = {
        'employee_id': [f'EMP_{i:05d}' for i in range(1, 251)],
        'first_name': np.random.choice(['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana'], 250),
        'last_name': np.random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia'], 250),
        'email': [f'emp_{i:05d}@deloitte.com' for i in range(1, 251)],
        'role': np.random.choice(['Consultant', 'Senior Consultant', 'Manager', 'Senior Manager'], 250),
        'service_line': np.random.choice(['Consulting', 'Financial Advisory', 'Risk Advisory', 'Technology'], 250),
        'location': np.random.choice(['Italy', 'Europe', 'EMEA'], 250),
        'company': np.random.choice(['Deloitte Consulting', 'Deloitte Advisory'], 250),
        'gender': np.random.choice(['Male', 'Female'], 250),
        'age': np.random.randint(25, 60, 250),
        'hire_date': [datetime.now() - timedelta(days=np.random.randint(30, 3650)) for _ in range(250)],
        'seniority_level': np.random.choice(['Analyst', 'Senior Analyst', 'Consultant', 'Senior Consultant', 'Manager'], 250),
        'attrition_risk': np.random.choice(['Low', 'Medium', 'High'], 250),
        'source': 'Qlik'
    }
    
    workforce_df = pd.DataFrame(employees)
    
    # Recruiting data
    candidates = {
        'candidate_id': [f'CAN_{i:05d}' for i in range(1, 151)],
        'first_name': np.random.choice(['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana'], 150),
        'last_name': np.random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia'], 150),
        'email': [f'can_{i:05d}@email.com' for i in range(1, 151)],
        'position_applied': np.random.choice(['Consultant', 'Senior Consultant', 'Manager'], 150),
        'service_line': np.random.choice(['Consulting', 'Financial Advisory', 'Risk Advisory', 'Technology'], 150),
        'location': np.random.choice(['Italy', 'Europe', 'EMEA'], 150),
        'company': np.random.choice(['Deloitte Consulting', 'Deloitte Advisory'], 150),
        'candidate_status': np.random.choice(['Pipeline', 'Screening', 'Interview', 'Offer', 'Hired', 'Rejected'], 150),
        'funnel_stage': np.random.choice(['Applied', 'Screening', 'Phone Interview', 'Technical Interview', 'Final Interview', 'Offer', 'Hired'], 150),
        'application_date': [datetime.now() - timedelta(days=np.random.randint(1, 180)) for _ in range(150)],
        'current_employer': np.random.choice(['Google', 'Microsoft', 'Amazon', 'Apple', 'Meta', 'Other'], 150),
        'gender': np.random.choice(['Male', 'Female'], 150),
        'age': np.random.randint(25, 50, 150),
        'source': 'Avature'
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
        
        st.markdown("### Login")
        
        user_id = st.text_input("User ID", placeholder="e.g., REC_001")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("Login", use_container_width=True, type="primary"):
            # Demo credentials
            demo_users = {
                "REC_001": {"password": "test123", "name": "John Recruiter", "role": "recruiter"},
                "REC_MGR_001": {"password": "test123", "name": "Jane Manager", "role": "manager"},
                "HRBP_001": {"password": "test123", "name": "Bob HRBP", "role": "hrbp"},
                "ADMIN_001": {"password": "test123", "name": "Alice Admin", "role": "admin"},
            }
            
            if user_id in demo_users and demo_users[user_id]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.user = demo_users[user_id]["name"]
                st.session_state.user_role = demo_users[user_id]["role"]
                st.success(f"Welcome, {st.session_state.user}!")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
        
        st.markdown("---")
        st.markdown("""
        **Demo Credentials:**
        - User: REC_001 | Password: test123 (Recruiter)
        - User: REC_MGR_001 | Password: test123 (Manager)
        - User: HRBP_001 | Password: test123 (HRBP)
        - User: ADMIN_001 | Password: test123 (Admin)
        """)

# ============================================================================
# MAIN APP
# ============================================================================

def show_main_app():
    """Mostra l'applicazione principale"""
    
    # Load demo data
    workforce_df, recruiting_df = generate_demo_data()
    
    # Sidebar
    with st.sidebar:
        st.title("🎯 HR Data Hub")
        
        # User info
        st.markdown(f"**User:** {st.session_state.user}")
        st.markdown(f"**Role:** {st.session_state.user_role.title()}")
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "👥 Workforce",
                "🎯 Recruiting",
                "🌈 Diversity",
                "📈 Capacity",
                "🔗 Integrated Analysis",
                "📋 Data Quality"
            ]
        )
        
        st.markdown("---")
        
        # Global filters
        st.subheader("Filters")
        
        service_lines = ["All"] + list(workforce_df['service_line'].unique())
        selected_sl = st.selectbox("Service Line", service_lines)
        
        locations = ["All"] + list(workforce_df['location'].unique())
        selected_loc = st.selectbox("Location", locations)
        
        genders = ["All", "Male", "Female"]
        selected_gender = st.selectbox("Gender", genders)
        
        st.markdown("---")
        
        # Logout
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.user_role = None
            st.rerun()
    
    # Apply filters
    filtered_workforce = workforce_df.copy()
    filtered_recruiting = recruiting_df.copy()
    
    if selected_sl != "All":
        filtered_workforce = filtered_workforce[filtered_workforce['service_line'] == selected_sl]
        filtered_recruiting = filtered_recruiting[filtered_recruiting['service_line'] == selected_sl]
    
    if selected_loc != "All":
        filtered_workforce = filtered_workforce[filtered_workforce['location'] == selected_loc]
        filtered_recruiting = filtered_recruiting[filtered_recruiting['location'] == selected_loc]
    
    if selected_gender != "All":
        filtered_workforce = filtered_workforce[filtered_workforce['gender'] == selected_gender]
        filtered_recruiting = filtered_recruiting[filtered_recruiting['gender'] == selected_gender]
    
    # Route to page
    if page == "📊 Dashboard":
        show_dashboard(filtered_workforce, filtered_recruiting)
    elif page == "👥 Workforce":
        show_workforce(filtered_workforce)
    elif page == "🎯 Recruiting":
        show_recruiting(filtered_recruiting)
    elif page == "🌈 Diversity":
        show_diversity(filtered_workforce, filtered_recruiting)
    elif page == "📈 Capacity":
        show_capacity(filtered_workforce)
    elif page == "🔗 Integrated Analysis":
        show_integrated_analysis(filtered_workforce, filtered_recruiting)
    elif page == "📋 Data Quality":
        show_data_quality(filtered_workforce, filtered_recruiting)

# ============================================================================
# PAGE: DASHBOARD
# ============================================================================

def show_dashboard(workforce_df, recruiting_df):
    """Dashboard principale"""
    st.title("📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Headcount", len(workforce_df))
    
    with col2:
        st.metric("🎯 Pipeline", len(recruiting_df))
    
    with col3:
        hired = len(recruiting_df[recruiting_df['candidate_status'] == 'Hired'])
        st.metric("✅ Hired", hired)
    
    with col4:
        rejected = len(recruiting_df[recruiting_df['candidate_status'] == 'Rejected'])
        st.metric("❌ Rejected", rejected)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sl_counts = workforce_df['service_line'].value_counts()
        fig = px.bar(
            x=sl_counts.index,
            y=sl_counts.values,
            title="Headcount by Service Line",
            labels={"x": "Service Line", "y": "Count"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        status_counts = recruiting_df['candidate_status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Candidate Status"
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: WORKFORCE
# ============================================================================

def show_workforce(workforce_df):
    """Pagina Workforce"""
    st.title("👥 Workforce")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Employees", len(workforce_df))
    
    with col2:
        male = len(workforce_df[workforce_df['gender'] == 'Male'])
        st.metric("Male", male)
    
    with col3:
        female = len(workforce_df[workforce_df['gender'] == 'Female'])
        st.metric("Female", female)
    
    with col4:
        high_risk = len(workforce_df[workforce_df['attrition_risk'] == 'High'])
        st.metric("High Risk", high_risk)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        seniority_counts = workforce_df['seniority_level'].value_counts()
        fig = px.bar(
            x=seniority_counts.index,
            y=seniority_counts.values,
            title="Seniority Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.histogram(
            workforce_df,
            x="age",
            nbins=20,
            title="Age Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Detailed Data")
    
    display_cols = ['first_name', 'last_name', 'email', 'role', 'service_line', 'location', 'gender', 'age', 'attrition_risk', 'source']
    st.dataframe(
        workforce_df[display_cols],
        use_container_width=True,
        height=400
    )

# ============================================================================
# PAGE: RECRUITING
# ============================================================================

def show_recruiting(recruiting_df):
    """Pagina Recruiting"""
    st.title("🎯 Recruiting")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Candidates", len(recruiting_df))
    
    with col2:
        hired = len(recruiting_df[recruiting_df['candidate_status'] == 'Hired'])
        st.metric("Hired", hired)
    
    with col3:
        pipeline = len(recruiting_df[recruiting_df['candidate_status'] == 'Pipeline'])
        st.metric("Pipeline", pipeline)
    
    with col4:
        rejected = len(recruiting_df[recruiting_df['candidate_status'] == 'Rejected'])
        st.metric("Rejected", rejected)
    
    st.markdown("---")
    
    if 'funnel_stage' in recruiting_df.columns:
        st.subheader("Recruiting Funnel")
        
        funnel_counts = recruiting_df['funnel_stage'].value_counts().sort_values(ascending=False)
        
        fig = go.Figure(go.Funnel(
            y=funnel_counts.index,
            x=funnel_counts.values
        ))
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Detailed Data")
    
    display_cols = ['first_name', 'last_name', 'email', 'position_applied', 'candidate_status', 'funnel_stage', 'application_date', 'current_employer', 'source']
    st.dataframe(
        recruiting_df[display_cols],
        use_container_width=True,
        height=400
    )

# ============================================================================
# PAGE: DIVERSITY
# ============================================================================

def show_diversity(workforce_df, recruiting_df):
    """Pagina Diversity"""
    st.title("🌈 Diversity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Workforce Gender")
        gender_counts = workforce_df['gender'].value_counts()
        fig = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="Gender Distribution (Workforce)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Pipeline Gender")
        gender_counts = recruiting_df['gender'].value_counts()
        fig = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="Gender Distribution (Pipeline)"
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: CAPACITY
# ============================================================================

def show_capacity(workforce_df):
    """Pagina Capacity"""
    st.title("📈 Capacity")
    
    st.info("Capacity planning data would be displayed here")
    
    capacity_by_sl = workforce_df.groupby('service_line').size()
    
    fig = px.bar(
        x=capacity_by_sl.index,
        y=capacity_by_sl.values,
        title="Headcount by Service Line"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: INTEGRATED ANALYSIS
# ============================================================================

def show_integrated_analysis(workforce_df, recruiting_df):
    """Pagina Integrated Analysis"""
    st.title("🔗 Integrated Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sl_workforce = workforce_df['service_line'].value_counts()
        fig = px.bar(
            x=sl_workforce.index,
            y=sl_workforce.values,
            title="Workforce by Service Line"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        sl_recruiting = recruiting_df['service_line'].value_counts()
        fig = px.bar(
            x=sl_recruiting.index,
            y=sl_recruiting.values,
            title="Pipeline by Service Line"
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: DATA QUALITY
# ============================================================================

def show_data_quality(workforce_df, recruiting_df):
    """Pagina Data Quality"""
    st.title("📋 Data Quality")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Workforce Records", len(workforce_df))
    
    with col2:
        st.metric("Recruiting Records", len(recruiting_df))
    
    with col3:
        total = len(workforce_df) + len(recruiting_df)
        st.metric("Total Records", total)
    
    with col4:
        st.metric("Data Sources", 2)
    
    st.markdown("---")
    st.info("✅ All data sources are fresh and up-to-date")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Punto di ingresso principale"""
    
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
