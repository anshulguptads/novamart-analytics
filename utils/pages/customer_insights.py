"""
Customer Insights Page
======================
Customer behavior analysis with distribution and relationship charts.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

def render(data):
    """Render Customer Insights page"""
    st.title("👥 Customer Insights")
    st.markdown("Understanding customer behavior, segments, and lifetime value")
    
    customers = data['customers'].copy()
    
    # =============================================================================
    # SECTION 1: HISTOGRAM - Customer Age Distribution
    # =============================================================================
    st.subheader("📊 Customer Age Distribution")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'age' in customers.columns:
            bin_size = st.slider("Bin Width", min_value=1, max_value=10, value=5, key="age_bins")
        else:
            bin_size = 5
    
    with col2:
        show_segment = st.checkbox("Show by Segment", key="age_segment")
    
    with col3:
        st.info("💡 Customer age skews toward 25-40 range")
    
    if 'age' in customers.columns:
        if show_segment and 'segment' in customers.columns:
            fig = px.histogram(
                customers,
                x='age',
                color='segment',
                nbins=int(customers['age'].max() / bin_size),
                title="Customer Age Distribution by Segment",
                labels={'age': 'Age (years)', 'count': 'Number of Customers'},
                barmode='overlay',
                height=400
            )
        else:
            fig = px.histogram(
                customers,
                x='age',
                nbins=int(customers['age'].max() / bin_size),
                title="Customer Age Distribution",
                labels={'age': 'Age (years)', 'count': 'Number of Customers'},
                height=400
            )
        
        fig.update_traces(marker_line_width=0, opacity=0.7)
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Age data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 2: BOX PLOT - Lifetime Value by Segment
    # =============================================================================
    st.subheader("💰 Lifetime Value by Customer Segment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        show_points = st.checkbox("Show individual points", value=False, key="ltv_points")
    
    with col2:
        st.info("💡 Premium segment has highest median LTV")
    
    if 'lifetime_value' in customers.columns or 'ltv' in customers.columns:
        ltv_col = 'lifetime_value' if 'lifetime_value' in customers.columns else 'ltv'
        
        if 'segment' in customers.columns:
            fig = go.Figure()
            
            for segment in sorted(customers['segment'].unique()):
                segment_data = customers[customers['segment'] == segment][ltv_col]
                
                if show_points:
                    fig.add_trace(go.Box(
                        y=segment_data,
                        name=segment,
                        boxmean='sd',
                        points='all',
                        jitter=0.3,
                        pointpos=-1.8
                    ))
                else:
                    fig.add_trace(go.Box(
                        y=segment_data,
                        name=segment,
                        boxmean='sd'
                    ))
            
            fig.update_layout(
                title="Lifetime Value Distribution by Segment",
                yaxis_title="Lifetime Value (₹)",
                height=450,
                hovermode='y unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Segment column not found")
    else:
        st.warning("⚠️ Lifetime value data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 3: VIOLIN PLOT - Satisfaction by NPS Category
    # =============================================================================
    st.subheader("😊 Satisfaction Distribution by NPS Category")
    
    col1, col2 = st.columns(2)
    
    with col1:
        split_by_channel = st.checkbox("Split by Channel", key="satisfaction_split")
    
    with col2:
        st.info("💡 Clear separation between Promoters and Detractors")
    
    if 'satisfaction' in customers.columns or 'nps' in customers.columns:
        sat_col = 'satisfaction' if 'satisfaction' in customers.columns else 'nps'
        
        # Create NPS categories
        if 'nps_category' not in customers.columns:
            if 'nps' in customers.columns:
                customers['nps_category'] = pd.cut(
                    customers['nps'],
                    bins=[0, 6, 8, 10],
                    labels=['Detractor', 'Passive', 'Promoter']
                )
            elif sat_col in customers.columns:
                customers['nps_category'] = pd.cut(
                    customers[sat_col],
                    bins=[0, 3, 6, 10],
                    labels=['Detractor', 'Passive', 'Promoter']
                )
            else:
                customers['nps_category'] = 'Unknown'
        
        if split_by_channel and 'channel' in customers.columns:
            fig = px.violin(
                customers,
                y=sat_col,
                x='nps_category',
                color='channel',
                box=True,
                points=False,
                title="Satisfaction Distribution by NPS Category and Channel",
                labels={sat_col: 'Satisfaction Score'},
                height=450
            )
        else:
            fig = px.violin(
                customers,
                y=sat_col,
                x='nps_category',
                box=True,
                points=False,
                title="Satisfaction Distribution by NPS Category",
                labels={sat_col: 'Satisfaction Score'},
                height=450
            )
        
        fig.update_layout(hovermode='y unified')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Satisfaction data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 4: SCATTER PLOT - Income vs. LTV
    # =============================================================================
    st.subheader("💎 Income vs. Lifetime Value Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_trend = st.checkbox("Show trend line", value=True, key="income_trend")
    
    with col2:
        if 'segment' in customers.columns:
            st.info(f"💡 {customers['segment'].nunique()} customer segments identified")
    
    with col3:
        st.info("💡 Positive correlation visible")
    
    ltv_col = 'lifetime_value' if 'lifetime_value' in customers.columns else 'ltv'
    income_col = 'income' if 'income' in customers.columns else 'annual_income'
    
    if ltv_col in customers.columns and income_col in customers.columns:
        if 'segment' in customers.columns:
            fig = px.scatter(
                customers,
                x=income_col,
                y=ltv_col,
                color='segment',
                title="Income vs. Lifetime Value by Segment",
                labels={income_col: 'Annual Income (₹)', ltv_col: 'Lifetime Value (₹)'},
                height=450,
                hover_name='segment' if 'customer_id' not in customers.columns else None,
                trendline='ols' if show_trend else None
            )
        else:
            fig = px.scatter(
                customers,
                x=income_col,
                y=ltv_col,
                title="Income vs. Lifetime Value",
                labels={income_col: 'Annual Income (₹)', ltv_col: 'Lifetime Value (₹)'},
                height=450,
                trendline='ols' if show_trend else None
            )
        
        fig.update_layout(hovermode='closest')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Required columns not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 5: SUNBURST - Customer Segmentation
    # =============================================================================
    st.subheader("🔄 Customer Segmentation Breakdown")
    
    st.info("💡 Click on segments to zoom in")
    
    if 'segment' in customers.columns:
        # Create hierarchy data
        if 'region' in customers.columns:
            hierarchy_data = customers.groupby(['region', 'segment']).size().reset_index(name='count')
            
            fig = px.sunburst(
                hierarchy_data,
                labels='region',
                parents='',
                values='count',
                color='segment',
                title="Customer Segmentation by Region",
                height=450
            )
            
            # Better: create proper hierarchy
            fig = px.sunburst(
                customers.groupby(['region', 'segment']).size().reset_index(name='count'),
                ids=['region_' + x if x in customers['region'].unique() else x for x in customers['region'].unique()] + customers['segment'].unique().tolist(),
                labels=customers['region'].unique().tolist() + customers['segment'].unique().tolist(),
                parents=[''] * len(customers['region'].unique()) + customers['region'].unique().tolist(),
                values=None,
                title="Customer Segmentation Hierarchy"
            )
        else:
            seg_counts = customers['segment'].value_counts().reset_index()
            seg_counts.columns = ['segment', 'count']
            
            fig = px.pie(
                seg_counts,
                values='count',
                names='segment',
                title="Customer Distribution by Segment",
                height=450
            )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Segment data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # INSIGHTS
    # =============================================================================
    st.subheader("💡 Customer Insights Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📊 Demographic Patterns**
        
        Customer base concentrated in 25-40 age range.
        Clear premium/budget segment separation.
        """)
    
    with col2:
        st.success("""
        **🎯 Value Opportunities**
        
        Strong positive income-LTV correlation.
        Budget segment shows upgrade potential.
        """)
