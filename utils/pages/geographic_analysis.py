"""
Geographic Analysis Page
========================
State-wise and location-based performance analysis.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def render(data):
    """Render Geographic Analysis page"""
    st.title("🗺️ Geographic Analysis")
    st.markdown("Analyze market performance across regions and states")
    
    geographic = data['geographic'].copy()
    
    # =============================================================================
    # SECTION 1: Top States by Revenue/Metrics
    # =============================================================================
    st.subheader("📊 State Performance Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        metric = st.selectbox(
            "Select Metric",
            ["Revenue", "Customers", "Market Penetration", "Satisfaction"],
            key="geo_metric"
        )
    
    with col2:
        limit = st.slider("Top N states", 5, 15, 10, key="top_n_states")
    
    with col3:
        st.info("💡 Maharashtra and Karnataka lead the market")
    
    # Map metric to column name
    metric_map = {
        'Revenue': 'revenue' if 'revenue' in geographic.columns else 'sales',
        'Customers': 'customers' if 'customers' in geographic.columns else 'customer_count',
        'Market Penetration': 'market_penetration' if 'market_penetration' in geographic.columns else 'penetration',
        'Satisfaction': 'satisfaction' if 'satisfaction' in geographic.columns else 'satisfaction_score'
    }
    
    metric_col = metric_map.get(metric)
    
    if metric_col and metric_col in geographic.columns:
        state_col = 'state' if 'state' in geographic.columns else 'region'
        
        top_states = geographic.nlargest(limit, metric_col)
        
        fig = px.bar(
            top_states,
            x=metric_col,
            y=state_col,
            orientation='h',
            title=f"Top {limit} States by {metric}",
            labels={metric_col: metric, state_col: 'State'},
            color=metric_col,
            color_continuous_scale='Viridis',
            height=450
        )
        
        fig.update_traces(text=top_states[metric_col], textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"⚠️ {metric} data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 2: Geographic Distribution
    # =============================================================================
    st.subheader("📍 Geographic Distribution")
    
    if 'revenue' in geographic.columns:
        state_col = 'state' if 'state' in geographic.columns else 'region'
        
        # Show state-wise breakdown
        geo_dist = geographic.groupby(state_col).agg({
            'revenue': 'sum' if 'revenue' in geographic.columns else 'mean',
            'customers': 'sum' if 'customers' in geographic.columns else 'mean'
        }).reset_index().sort_values('revenue', ascending=False)
        
        fig = px.pie(
            geo_dist,
            values='revenue',
            names=state_col,
            title="Revenue Distribution by State",
            height=450
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Geographic distribution data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 3: Multi-Metric Comparison
    # =============================================================================
    st.subheader("📊 Multi-Metric Geographic Comparison")
    
    if 'revenue' in geographic.columns and 'customers' in geographic.columns:
        state_col = 'state' if 'state' in geographic.columns else 'region'
        
        # Prepare data for scatter plot
        top_10_states = geographic.nlargest(10, 'revenue')
        
        fig = px.scatter(
            top_10_states,
            x='customers',
            y='revenue',
            size='customers',
            color=state_col,
            hover_name=state_col,
            title="Revenue vs. Customer Count by State (Top 10)",
            labels={'revenue': 'Revenue (₹)', 'customers': 'Number of Customers'},
            height=450
        )
        
        fig.update_layout(hovermode='closest')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Required geographic metrics not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 4: Satisfaction & Growth Analysis
    # =============================================================================
    st.subheader("😊 Satisfaction & Market Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'satisfaction' in geographic.columns:
            state_col = 'state' if 'state' in geographic.columns else 'region'
            
            satisfaction_data = geographic.nlargest(10, 'revenue').sort_values('satisfaction', ascending=True)
            
            fig = px.bar(
                satisfaction_data,
                x='satisfaction',
                y=state_col,
                orientation='h',
                title="Customer Satisfaction by Top States",
                labels={'satisfaction': 'Satisfaction Score', state_col: 'State'},
                color='satisfaction',
                color_continuous_scale='RdYlGn',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.info("""
        **🎯 Market Insights**
        
        **Strong Performers:**
        - Maharashtra & Karnataka
        - High revenue + Good satisfaction
        
        **Growth Opportunities:**
        - Eastern states
        - Lower penetration but growth potential
        """)
    
    st.markdown("---")
    
    # =============================================================================
    # KEY INSIGHTS
    # =============================================================================
    st.subheader("💡 Geographic Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **🌟 Metropolitan Dominance**
        
        Tier 1 cities drive 60%+ of revenue.
        Premium segment concentration in metros.
        """)
    
    with col2:
        st.info("""
        **🚀 Growth Potential**
        
        Tier 2/3 cities show rapid growth.
        Budget segment expansion opportunity.
        """)
