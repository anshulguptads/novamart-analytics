"""
Attribution & Funnel Page
=========================
Attribution models and marketing funnel analysis.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def render(data):
    """Render Attribution & Funnel page"""
    st.title("🎯 Attribution & Funnel Analysis")
    st.markdown("Understand customer journey and channel attribution")
    
    # =============================================================================
    # SECTION 1: FUNNEL CHART
    # =============================================================================
    st.subheader("📊 Marketing Funnel")
    
    funnel = data['funnel'].copy()
    
    if 'stage' in funnel.columns and 'visitors' in funnel.columns:
        # Sort by conversion order
        stage_order = ['Awareness', 'Interest', 'Consideration', 'Evaluation', 'Decision', 'Purchase']
        funnel['stage_order'] = funnel['stage'].apply(lambda x: stage_order.index(x) if x in stage_order else 999)
        funnel = funnel.sort_values('stage_order').drop('stage_order', axis=1)
        
        # Calculate conversion rates
        funnel['conversion_rate'] = (funnel['visitors'].shift(1) / funnel['visitors'].shift(1).iloc[0] * 100).fillna(100)
        funnel['stage_to_next'] = (funnel['visitors'] / funnel['visitors'].shift(1) * 100).fillna(100)
        
        # Create funnel chart
        fig = go.Figure(go.Funnel(
            y=funnel['stage'],
            x=funnel['visitors'],
            textposition='inside',
            textinfo='value+percent',
            hovertemplate='<b>%{y}</b><br>Visitors: %{x:,}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Marketing Conversion Funnel",
            height=450,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show conversion rates
        st.info("📊 Conversion Rates Between Stages")
        funnel_display = funnel[['stage', 'visitors', 'stage_to_next']].copy()
        funnel_display.columns = ['Stage', 'Visitors', 'Conversion Rate (%)']
        funnel_display['Conversion Rate (%)'] = funnel_display['Conversion Rate (%)'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "-")
        
        st.dataframe(funnel_display, use_container_width=True)
        
        # Insights
        max_drop = funnel['stage_to_next'].idxmin()
        st.warning(f"""
        **⚠️ Largest Drop-off:** {funnel.loc[max_drop, 'stage']} stage
        
        Focus optimization efforts on top-of-funnel conversion.
        """)
    else:
        st.warning("⚠️ Funnel data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 2: ATTRIBUTION MODEL COMPARISON
    # =============================================================================
    st.subheader("🏆 Attribution Model Comparison")
    
    attribution = data['attribution'].copy()
    
    if 'channel' in attribution.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            attribution_model = st.selectbox(
                "Select Attribution Model",
                [col for col in attribution.columns if col != 'channel'] if 'channel' in attribution.columns else [],
                key="attribution_model"
            )
        
        with col2:
            st.info("💡 Compare how attribution models credit different channels")
        
        if attribution_model and attribution_model in attribution.columns:
            attr_data = attribution[['channel', attribution_model]].sort_values(attribution_model, ascending=False)
            
            fig = px.bar(
                attr_data,
                x=attribution_model,
                y='channel',
                orientation='h',
                title=f"Channel Attribution - {attribution_model}",
                labels={attribution_model: 'Attribution %', 'channel': 'Channel'},
                color=attribution_model,
                color_continuous_scale='Blues',
                height=400
            )
            
            fig.update_traces(text=attr_data[attribution_model], textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Attribution data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 3: CORRELATION HEATMAP
    # =============================================================================
    st.subheader("🔥 Metric Correlation Matrix")
    
    correlation = data['correlation']
    
    if correlation is not None and len(correlation) > 0:
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=correlation.values,
            x=correlation.columns,
            y=correlation.index,
            colorscale='RdBu',
            zmid=0,
            text=correlation.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="Marketing Metrics Correlation Matrix",
            xaxis_title="Metrics",
            yaxis_title="Metrics",
            height=600,
            width=800
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.info("""
        **📊 Correlation Insights**
        
        **Positive Correlations:**
        - Spend, Impressions, Clicks highly correlated
        - Revenue correlates with conversions
        
        **Negative Correlations:**
        - ROAS decreases with higher spend (diminishing returns)
        - Cart abandonment inversely relates to conversions
        """)
    else:
        st.warning("⚠️ Correlation data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 4: DONUT CHART - Attribution Comparison
    # =============================================================================
    st.subheader("🍩 Multi-Model Attribution View")
    
    if 'channel' in attribution.columns:
        # Get all attribution model columns
        model_cols = [col for col in attribution.columns if col != 'channel']
        
        if len(model_cols) >= 2:
            col1, col2 = st.columns(2)
            
            with col1:
                model1 = st.selectbox("First Model", model_cols, index=0, key="model1")
            with col2:
                model2 = st.selectbox("Second Model", model_cols, index=1 if len(model_cols) > 1 else 0, key="model2")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if model1:
                    data1 = attribution[['channel', model1]].sort_values(model1, ascending=False).head(8)
                    fig1 = px.pie(
                        data1,
                        values=model1,
                        names='channel',
                        title=f"Attribution: {model1}",
                        hole=0.4
                    )
                    st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                if model2:
                    data2 = attribution[['channel', model2]].sort_values(model2, ascending=False).head(8)
                    fig2 = px.pie(
                        data2,
                        values=model2,
                        names='channel',
                        title=f"Attribution: {model2}",
                        hole=0.4
                    )
                    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # =============================================================================
    # KEY INSIGHTS
    # =============================================================================
    st.subheader("💡 Attribution & Funnel Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📊 Funnel Optimization**
        
        Biggest drop-off at top-of-funnel.
        Increase awareness/interest activities.
        """)
    
    with col2:
        st.success("""
        **🎯 Attribution Insights**
        
        Different models credit channels differently.
        Use linear attribution for balanced view.
        """)
