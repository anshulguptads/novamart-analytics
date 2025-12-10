"""
NovaMart Marketing Analytics Dashboard
======================================
Masters of AI in Business - Data Visualization Assignment

A comprehensive Streamlit dashboard showcasing marketing analytics,
customer insights, product performance, geographic analysis, and ML model evaluation.

To run locally: streamlit run app.py
To deploy to Streamlit Cloud: Push this repo to GitHub and connect it via Streamlit Cloud dashboard.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent / "utils"))

from data_loader import load_all_data
from pages import (
    executive_overview,
    campaign_analytics,
    customer_insights,
    product_performance,
    geographic_analysis,
    attribution_funnel,
    ml_model_evaluation
)

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="NovaMart Marketing Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================
def render_sidebar():
    """Create sidebar navigation and return selected page"""
    with st.sidebar:
        st.title("📊 NovaMart Analytics")
        st.markdown("---")
        
        page = st.radio(
            "Navigate to:",
            [
                "🏠 Executive Overview",
                "📈 Campaign Analytics",
                "👥 Customer Insights",
                "📦 Product Performance",
                "🗺️ Geographic Analysis",
                "🎯 Attribution & Funnel",
                "🤖 ML Model Evaluation"
            ],
            index=0
        )
        
        st.markdown("---")
        st.markdown("""
        **About This Dashboard**
        
        Built with ❤️ using Streamlit, Plotly & Pandas
        
        **Dataset Overview:**
        - 11 integrated CSV files
        - Multi-channel marketing data
        - Customer segmentation & behavior
        - ML model performance metrics
        
        **Features:**
        - 20+ interactive visualizations
        - Real-time filters & drills
        - Business insights & KPIs
        - Model evaluation tools
        """)
        st.markdown("---")
        st.caption("Masters of AI in Business\nData Visualization Assignment")
    
    return page

# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    """Main application logic"""
    
    # Load data with caching
    data = load_all_data()
    
    if data is None:
        st.error("❌ Failed to load data. Please check the data files.")
        st.info("Ensure all CSV files are in the `data/` folder relative to this script.")
        return
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Route to appropriate page
    if page == "🏠 Executive Overview":
        executive_overview.render(data)
    
    elif page == "📈 Campaign Analytics":
        campaign_analytics.render(data)
    
    elif page == "👥 Customer Insights":
        customer_insights.render(data)
    
    elif page == "📦 Product Performance":
        product_performance.render(data)
    
    elif page == "🗺️ Geographic Analysis":
        geographic_analysis.render(data)
    
    elif page == "🎯 Attribution & Funnel":
        attribution_funnel.render(data)
    
    elif page == "🤖 ML Model Evaluation":
        ml_model_evaluation.render(data)

if __name__ == "__main__":
    main()
