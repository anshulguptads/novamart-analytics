"""
Data Loading Utilities with Caching
===================================
Handles loading and preprocessing of all datasets with Streamlit caching.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# DATA LOADING WITH CACHING
# =============================================================================
@st.cache_data
def load_all_data():
    """
    Load all required datasets with caching.
    
    Returns:
        dict: Dictionary containing all loaded dataframes, or None if loading fails
    """
    data = {}
    
    # Try to find data folder - it could be in 'data/' or relative to this script
    data_paths = [
        Path(__file__).parent.parent / "NovaMart_Marketing_Analytics_Dataset" / "marketing_dataset",
        Path(__file__).parent.parent / "data",
        Path("data"),
        Path("marketing_dataset"),
    ]
    
    data_path = None
    for path in data_paths:
        if path.exists():
            data_path = path
            break
    
    if data_path is None:
        st.error("❌ Data folder not found!")
        st.info("Please ensure your data folder is in one of these locations:\n" +
                "\n".join([f"- {p}" for p in data_paths]))
        return None
    
    try:
        # Campaign data - parse date column
        data['campaigns'] = pd.read_csv(
            data_path / "campaign_performance.csv",
            parse_dates=['date'] if 'date' in pd.read_csv(data_path / "campaign_performance.csv", nrows=0).columns else False
        )
        
        # Customer data
        data['customers'] = pd.read_csv(data_path / "customer_data.csv")
        
        # Product sales data
        data['products'] = pd.read_csv(data_path / "product_sales.csv")
        
        # Lead scoring results
        data['leads'] = pd.read_csv(data_path / "lead_scoring_results.csv")
        
        # Feature importance
        data['feature_importance'] = pd.read_csv(data_path / "feature_importance.csv")
        
        # Learning curve
        data['learning_curve'] = pd.read_csv(data_path / "learning_curve.csv")
        
        # Geographic data
        data['geographic'] = pd.read_csv(data_path / "geographic_data.csv")
        
        # Attribution model
        data['attribution'] = pd.read_csv(data_path / "channel_attribution.csv")
        
        # Funnel data
        data['funnel'] = pd.read_csv(data_path / "funnel_data.csv")
        
        # Customer journey
        data['journey'] = pd.read_csv(data_path / "customer_journey.csv")
        
        # Correlation matrix
        data['correlation'] = pd.read_csv(data_path / "correlation_matrix.csv", index_col=0)
        
        return data
    
    except FileNotFoundError as e:
        st.error(f"❌ Data file not found: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None

# =============================================================================
# DATA PREPROCESSING UTILITIES
# =============================================================================
@st.cache_data
def preprocess_campaign_data(campaigns):
    """Preprocess campaign data for analysis"""
    df = campaigns.copy()
    
    # Ensure date column is datetime
    if 'date' in df.columns and df['date'].dtype != 'datetime64[ns]':
        df['date'] = pd.to_datetime(df['date'])
    
    # Add time-based features
    if 'date' in df.columns:
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['week'] = df['date'].dt.isocalendar().week
        df['dayofweek'] = df['date'].dt.day_name()
        df['month_name'] = df['date'].dt.strftime('%B')
    
    return df

@st.cache_data
def preprocess_customer_data(customers):
    """Preprocess customer data for analysis"""
    df = customers.copy()
    
    # Handle missing values
    df = df.fillna(df.mean(numeric_only=True))
    
    return df

@st.cache_data
def get_summary_stats(campaigns):
    """Calculate summary statistics"""
    if campaigns is None:
        return {}
    
    campaigns = preprocess_campaign_data(campaigns)
    
    return {
        'total_revenue': campaigns['revenue'].sum() if 'revenue' in campaigns.columns else 0,
        'total_conversions': campaigns['conversions'].sum() if 'conversions' in campaigns.columns else 0,
        'avg_roas': campaigns['roas'].mean() if 'roas' in campaigns.columns else 0,
        'total_spend': campaigns['spend'].sum() if 'spend' in campaigns.columns else 0,
    }

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
def get_channel_options(campaigns):
    """Get list of available channels"""
    if 'channel' in campaigns.columns:
        return sorted(campaigns['channel'].unique().tolist())
    return []

def get_region_options(campaigns):
    """Get list of available regions"""
    if 'region' in campaigns.columns:
        return sorted(campaigns['region'].unique().tolist())
    return []

def get_year_options(campaigns):
    """Get list of available years"""
    campaigns = preprocess_campaign_data(campaigns)
    if 'year' in campaigns.columns:
        return sorted(campaigns['year'].unique().tolist())
    return []
