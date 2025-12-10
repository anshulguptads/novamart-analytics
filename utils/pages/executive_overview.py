"""
Executive Overview Page
=======================
Key performance metrics and high-level dashboard view.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from data_loader import preprocess_campaign_data, get_summary_stats

def render(data):
    """Render Executive Overview page"""
    st.title("🏠 Executive Overview")
    st.markdown("Key performance metrics and revenue trends at a glance")
    
    campaigns = preprocess_campaign_data(data['campaigns'])
    
    # =============================================================================
    # KPI CARDS
    # =============================================================================
    st.subheader("📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = campaigns['revenue'].sum() if 'revenue' in campaigns.columns else 0
        st.metric(
            label="Total Revenue",
            value=f"₹{total_revenue:,.0f}",
            delta=f"+{campaigns['revenue'].iloc[-30:].sum() / campaigns['revenue'].sum() * 100:.1f}% (Last 30 days)"
        )
    
    with col2:
        total_conversions = campaigns['conversions'].sum() if 'conversions' in campaigns.columns else 0
        st.metric(
            label="Total Conversions",
            value=f"{total_conversions:,.0f}",
            delta=f"{campaigns['conversions'].mean():.0f} avg/day"
        )
    
    with col3:
        avg_roas = campaigns['roas'].mean() if 'roas' in campaigns.columns else 0
        st.metric(
            label="Avg ROAS",
            value=f"{avg_roas:.2f}x",
            delta="Return on Ad Spend"
        )
    
    with col4:
        total_spend = campaigns['spend'].sum() if 'spend' in campaigns.columns else 0
        st.metric(
            label="Total Ad Spend",
            value=f"₹{total_spend:,.0f}",
            delta=f"ROI: ₹{(total_revenue - total_spend):,.0f}"
        )
    
    st.markdown("---")
    
    # =============================================================================
    # REVENUE TREND LINE CHART
    # =============================================================================
    st.subheader("📈 Revenue Trend Over Time")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        aggregation = st.selectbox(
            "Aggregation Level",
            ["Daily", "Weekly", "Monthly"],
            key="agg_trend"
        )
    
    with col2:
        if 'channel' in campaigns.columns:
            channels = st.multiselect(
                "Filter by Channel",
                options=campaigns['channel'].unique().tolist(),
                default=campaigns['channel'].unique().tolist(),
                key="channels_trend"
            )
        else:
            channels = None
    
    with col3:
        st.info("💡 Hover over the chart for daily values")
    
    # Filter by channel if selected
    trend_data = campaigns.copy()
    if channels:
        trend_data = trend_data[trend_data['channel'].isin(channels)]
    
    # Aggregate data
    if aggregation == "Daily":
        trend_df = trend_data.groupby('date')['revenue'].sum().reset_index()
        x_title = "Date"
    elif aggregation == "Weekly":
        trend_data['week_start'] = trend_data['date'] - pd.to_timedelta(trend_data['date'].dt.dayofweek, unit='d')
        trend_df = trend_data.groupby('week_start')['revenue'].sum().reset_index()
        trend_df.columns = ['date', 'revenue']
        x_title = "Week Starting"
    else:  # Monthly
        trend_data['year_month'] = trend_data['date'].dt.to_period('M')
        trend_df = trend_data.groupby('year_month')['revenue'].sum().reset_index()
        trend_df['date'] = trend_df['year_month'].dt.to_timestamp()
        trend_df = trend_df[['date', 'revenue']]
        x_title = "Month"
    
    # Create line chart
    fig = px.line(
        trend_df,
        x='date',
        y='revenue',
        title="Revenue Trend",
        labels={'revenue': 'Revenue (₹)', 'date': x_title},
        markers=True,
        line_shape='spline'
    )
    fig.update_traces(line=dict(width=2))
    fig.update_layout(hovermode='x unified', height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # =============================================================================
    # CHANNEL PERFORMANCE BAR CHART
    # =============================================================================
    st.subheader("💼 Channel Performance Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric = st.selectbox(
            "Select Metric",
            ["Revenue", "Conversions", "ROAS"],
            key="metric_channel"
        )
    
    with col2:
        st.info(f"📊 Comparing channels by {metric.lower()}")
    
    if 'channel' in campaigns.columns:
        # Aggregate by channel
        if metric == "Revenue":
            channel_data = campaigns.groupby('channel')['revenue'].sum().sort_values(ascending=True)
            y_label = "Revenue (₹)"
        elif metric == "Conversions":
            channel_data = campaigns.groupby('channel')['conversions'].sum().sort_values(ascending=True)
            y_label = "Conversions"
        else:  # ROAS
            channel_data = campaigns.groupby('channel')['roas'].mean().sort_values(ascending=True)
            y_label = "ROAS"
        
        fig = go.Figure(data=[
            go.Bar(
                y=channel_data.index,
                x=channel_data.values,
                orientation='h',
                marker=dict(
                    color=channel_data.values,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title=metric)
                ),
                text=[f"{v:,.0f}" if metric != "ROAS" else f"{v:.2f}x" for v in channel_data.values],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title=f"Channel Performance by {metric}",
            xaxis_title=y_label,
            yaxis_title="Channel",
            height=400,
            showlegend=False,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Channel data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # INSIGHTS SECTION
    # =============================================================================
    st.subheader("💡 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **📈 Strong Revenue Growth**
        
        The dashboard shows consistent revenue growth with clear seasonal patterns.
        Peak periods align with major shopping seasons.
        """)
    
    with col2:
        st.success("""
        **✅ Efficient Marketing Spend**
        
        ROAS metrics indicate healthy return on marketing investment.
        Multi-channel approach diversifies risk and reaches wider audience.
        """)
    
    with col3:
        st.warning("""
        **🎯 Optimization Opportunity**
        
        Some channels show lower conversion rates.
        Further analysis recommended for budget reallocation.
        """)
