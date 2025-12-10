"""
Product Performance Page
========================
Product sales and hierarchy analysis.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def render(data):
    """Render Product Performance page"""
    st.title("📦 Product Performance")
    st.markdown("Analyze product sales, margins, and hierarchical relationships")
    
    products = data['products'].copy()
    
    # =============================================================================
    # SECTION 1: TREEMAP - Product Sales Hierarchy
    # =============================================================================
    st.subheader("🌳 Product Hierarchy Treemap")
    
    st.info("💡 Click on categories to drill down. Size = Sales, Color = Profit Margin")
    
    # Check for hierarchy columns
    category_col = 'category' if 'category' in products.columns else None
    subcategory_col = 'subcategory' if 'subcategory' in products.columns else None
    product_col = 'product' if 'product' in products.columns else None
    sales_col = 'sales' if 'sales' in products.columns else None
    margin_col = 'profit_margin' if 'profit_margin' in products.columns else 'margin'
    
    if category_col and sales_col:
        # Prepare hierarchical data
        if subcategory_col:
            hierarchy_data = products.groupby([category_col, subcategory_col]).agg({
                sales_col: 'sum',
                margin_col: 'mean'
            }).reset_index()
            hierarchy_data['parent'] = hierarchy_data[category_col]
            hierarchy_data['label'] = hierarchy_data[subcategory_col]
            hierarchy_data['id'] = hierarchy_data[category_col] + '_' + hierarchy_data[subcategory_col]
        else:
            hierarchy_data = products.groupby(category_col).agg({
                sales_col: 'sum',
                margin_col: 'mean'
            }).reset_index()
            hierarchy_data['parent'] = ''
            hierarchy_data['label'] = hierarchy_data[category_col]
            hierarchy_data['id'] = hierarchy_data[category_col]
        
        # Create treemap
        fig = px.treemap(
            hierarchy_data,
            ids='id',
            labels='label',
            parents='parent',
            values=sales_col,
            color=margin_col,
            color_continuous_scale='RdYlGn',
            title="Product Sales Hierarchy by Category and Margin",
            height=500
        )
        
        fig.update_traces(textposition='middle center')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Required product hierarchy columns not found")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 2: Category Performance Comparison
    # =============================================================================
    st.subheader("📊 Category Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric = st.selectbox(
            "Select Metric",
            ["Sales", "Units", "Profit Margin"],
            key="category_metric"
        )
    
    with col2:
        st.info("💡 Compare categories across different metrics")
    
    if category_col and sales_col:
        if metric == "Sales":
            metric_col = sales_col
            agg_func = 'sum'
        elif metric == "Units":
            metric_col = 'units' if 'units' in products.columns else sales_col
            agg_func = 'sum'
        else:
            metric_col = margin_col
            agg_func = 'mean'
        
        cat_data = products.groupby(category_col)[metric_col].agg(agg_func).sort_values(ascending=False)
        
        fig = px.bar(
            x=cat_data.values,
            y=cat_data.index,
            orientation='h',
            title=f"Category Performance by {metric}",
            labels={'x': metric, 'y': 'Category'},
            color=cat_data.values,
            color_continuous_scale='Viridis',
            height=400
        )
        
        fig.update_traces(text=cat_data.values, textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Category data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 3: Regional Product Performance
    # =============================================================================
    st.subheader("🗺️ Regional Product Performance")
    
    if 'region' in products.columns and category_col and sales_col:
        region = st.selectbox(
            "Select Region",
            ["All"] + sorted(products['region'].unique().tolist()),
            key="region_product"
        )
        
        if region != "All":
            regional_products = products[products['region'] == region]
        else:
            regional_products = products
        
        # Get top products by sales
        top_products = regional_products.groupby(category_col)[sales_col].sum().nlargest(10)
        
        fig = px.bar(
            x=top_products.values,
            y=top_products.index,
            orientation='h',
            title=f"Top Categories by Sales - {region if region != 'All' else 'All Regions'}",
            labels={'x': 'Sales (₹)', 'y': 'Category'},
            color=top_products.values,
            color_continuous_scale='Plasma',
            height=400
        )
        
        fig.update_traces(text=top_products.values, textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Regional product data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 4: Quarterly Trends
    # =============================================================================
    st.subheader("📈 Quarterly Sales Trends")
    
    if 'quarter' in products.columns and category_col and sales_col:
        quarterly_data = products.groupby(['quarter', category_col])[sales_col].sum().reset_index()
        
        fig = px.line(
            quarterly_data,
            x='quarter',
            y=sales_col,
            color=category_col,
            markers=True,
            title="Quarterly Sales by Category",
            labels={'quarter': 'Quarter', sales_col: 'Sales (₹)'},
            height=450
        )
        
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Quarterly data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # KEY INSIGHTS
    # =============================================================================
    st.subheader("💡 Product Performance Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📊 Sales Distribution**
        
        Electronics dominates sales volume.
        Fashion shows strongest profit margins.
        """)
    
    with col2:
        st.success("""
        **🎯 Pricing Opportunity**
        
        Review high-volume low-margin products.
        Consider bundle strategies for margin improvement.
        """)
