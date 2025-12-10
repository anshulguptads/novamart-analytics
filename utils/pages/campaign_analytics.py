"""
Campaign Analytics Page
=======================
Detailed campaign performance analysis with temporal and comparison charts.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from data_loader import preprocess_campaign_data

def render(data):
    """Render Campaign Analytics page"""
    st.title("📈 Campaign Analytics")
    st.markdown("Deep dive into campaign performance across channels and regions")
    
    campaigns = preprocess_campaign_data(data['campaigns'])
    
    # =============================================================================
    # SECTION 1: GROUPED BAR CHART - Regional Performance by Quarter
    # =============================================================================
    st.subheader("📊 Regional Performance by Quarter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'year' in campaigns.columns:
            year = st.selectbox(
                "Select Year",
                sorted(campaigns['year'].unique()),
                key="year_regional"
            )
        else:
            year = None
    
    with col2:
        st.info("💡 Compare revenue across regions by quarter")
    
    if year and 'region' in campaigns.columns and 'quarter' in campaigns.columns:
        regional_data = campaigns[campaigns['year'] == year].groupby(['quarter', 'region'])['revenue'].sum().reset_index()
        
        fig = px.bar(
            regional_data,
            x='quarter',
            y='revenue',
            color='region',
            barmode='group',
            title=f"Regional Revenue by Quarter ({year})",
            labels={'revenue': 'Revenue (₹)', 'quarter': 'Quarter'},
            height=450
        )
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insight
        top_region = regional_data.groupby('region')['revenue'].sum().idxmax()
        st.success(f"✅ **{top_region}** region showed the strongest performance in {year}")
    else:
        st.warning("⚠️ Required time-based columns not found in data")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 2: STACKED BAR CHART - Campaign Type Contribution
    # =============================================================================
    st.subheader("📌 Campaign Type Contribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        stacked_view = st.radio(
            "View Type",
            ["Absolute Values", "100% Stacked"],
            key="stacked_view"
        )
    
    with col2:
        st.info("💡 See how different campaign types contribute to spend")
    
    if 'campaign_type' in campaigns.columns or 'campaign_name' in campaigns.columns:
        campaign_col = 'campaign_type' if 'campaign_type' in campaigns.columns else 'campaign_name'
        
        # Group by month and campaign type
        campaigns['year_month'] = campaigns['date'].dt.to_period('M')
        campaign_type_data = campaigns.groupby(['year_month', campaign_col])['spend'].sum().reset_index()
        campaign_type_data['date'] = campaign_type_data['year_month'].dt.to_timestamp()
        
        if stacked_view == "100% Stacked":
            # Convert to percentage
            campaign_type_data = campaign_type_data.copy()
            totals = campaign_type_data.groupby('date')['spend'].sum()
            campaign_type_data['percentage'] = campaign_type_data.apply(
                lambda row: (row['spend'] / totals[row['date']] * 100), axis=1
            )
            
            fig = px.bar(
                campaign_type_data,
                x='date',
                y='percentage',
                color=campaign_col,
                title="Campaign Type Contribution (100% Stacked)",
                labels={'percentage': 'Percentage (%)', 'date': 'Month'},
                barmode='stack',
                height=450
            )
        else:
            fig = px.bar(
                campaign_type_data,
                x='date',
                y='spend',
                color=campaign_col,
                title="Campaign Type Contribution (Absolute)",
                labels={'spend': 'Spend (₹)', 'date': 'Month'},
                barmode='stack',
                height=450
            )
        
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Campaign type column not found in data")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 3: CUMULATIVE CONVERSIONS AREA CHART
    # =============================================================================
    st.subheader("📊 Cumulative Conversions by Channel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'region' in campaigns.columns:
            region = st.selectbox(
                "Filter by Region",
                ["All"] + sorted(campaigns['region'].unique().tolist()),
                key="region_cumulative"
            )
        else:
            region = "All"
    
    with col2:
        st.info("💡 See cumulative conversion trends by channel")
    
    if 'channel' in campaigns.columns:
        area_data = campaigns.copy()
        
        if region != "All":
            area_data = area_data[area_data['region'] == region]
        
        # Calculate cumulative conversions
        area_data = area_data.sort_values('date')
        area_data['cumulative_conversions'] = area_data.groupby('channel')['conversions'].cumsum()
        
        fig = px.area(
            area_data,
            x='date',
            y='cumulative_conversions',
            color='channel',
            title=f"Cumulative Conversions by Channel{f' - {region}' if region != 'All' else ''}",
            labels={'cumulative_conversions': 'Cumulative Conversions', 'date': 'Date'},
            height=450
        )
        
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Channel column not found in data")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 4: CALENDAR HEATMAP
    # =============================================================================
    st.subheader("📅 Daily Performance Heatmap")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'year' in campaigns.columns:
            year_heatmap = st.selectbox(
                "Select Year",
                sorted(campaigns['year'].unique()),
                key="year_heatmap"
            )
        else:
            year_heatmap = None
    
    with col2:
        metric_heatmap = st.selectbox(
            "Select Metric",
            ["Revenue", "Conversions", "Spend"],
            key="metric_heatmap"
        )
    
    if year_heatmap:
        heatmap_data = campaigns[campaigns['year'] == year_heatmap].copy()
        
        if metric_heatmap == "Revenue":
            metric_col = 'revenue'
        elif metric_heatmap == "Conversions":
            metric_col = 'conversions'
        else:
            metric_col = 'spend'
        
        # Prepare data for calendar heatmap
        heatmap_daily = heatmap_data.groupby('date')[metric_col].sum().reset_index()
        heatmap_daily['month'] = heatmap_daily['date'].dt.month
        heatmap_daily['day'] = heatmap_daily['date'].dt.day
        heatmap_daily['week'] = heatmap_daily['date'].dt.isocalendar().week
        heatmap_daily['month_name'] = heatmap_daily['date'].dt.strftime('%B')
        
        # Create pivot for heatmap
        pivot_data = heatmap_daily.pivot_table(
            values=metric_col,
            index='month',
            columns='week',
            aggfunc='sum'
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][:len(pivot_data)],
            colorscale='YlOrRd',
            hovertemplate='<b>Week %{x}</b><br>Month: %{y}<br>' + metric_heatmap + ': %{z:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Daily {metric_heatmap} Heatmap - {year_heatmap}",
            xaxis_title="Week Number",
            yaxis_title="Month",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Year data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # KEY INSIGHTS
    # =============================================================================
    st.subheader("💡 Campaign Analytics Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📈 Seasonal Patterns**
        
        Q4 shows significant boost due to festive season.
        Plan budget allocation accordingly.
        """)
    
    with col2:
        st.success("""
        **🎯 Multi-Channel Strategy**
        
        Diverse channels reduce risk and reach multiple segments.
        Channel-specific optimization recommended.
        """)
