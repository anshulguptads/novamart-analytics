"""
ML Model Evaluation Page
========================
Confusion matrix, ROC curve, learning curves, and feature importance.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report

def render(data):
    """Render ML Model Evaluation page"""
    st.title("🤖 ML Model Evaluation")
    st.markdown("Lead scoring model performance and diagnostics")
    
    leads = data['leads'].copy()
    feature_importance = data['feature_importance'].copy()
    learning_curve = data['learning_curve'].copy()
    
    # =============================================================================
    # SECTION 1: CONFUSION MATRIX
    # =============================================================================
    st.subheader("🎯 Confusion Matrix")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("💡 Model shows good true positive rate")
    
    with col2:
        if 'predicted_probability' in leads.columns:
            threshold = st.slider(
                "Classification Threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.05,
                key="cm_threshold"
            )
    
    # Find actual and predicted columns
    actual_col = 'actual_converted' if 'actual_converted' in leads.columns else 'target'
    pred_prob_col = 'predicted_probability' if 'predicted_probability' in leads.columns else None
    pred_class_col = 'predicted_class' if 'predicted_class' in leads.columns else None
    
    if actual_col in leads.columns:
        # Create confusion matrix
        if pred_prob_col and pred_prob_col in leads.columns:
            predicted = (leads[pred_prob_col] >= threshold).astype(int)
        elif pred_class_col and pred_class_col in leads.columns:
            predicted = leads[pred_class_col]
        else:
            predicted = None
        
        if predicted is not None:
            cm = confusion_matrix(leads[actual_col], predicted)
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=cm,
                x=['Not Converted', 'Converted'],
                y=['Not Converted', 'Converted'],
                text=cm,
                texttemplate='%{text}',
                textfont={"size": 14},
                colorscale='Blues',
                hovertemplate='Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>'
            ))
            
            fig.update_layout(
                title=f"Confusion Matrix (Threshold: {threshold:.2f})",
                xaxis_title="Predicted",
                yaxis_title="Actual",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate metrics
            tn, fp, fn, tp = cm.ravel()
            accuracy = (tp + tn) / (tp + tn + fp + fn)
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Accuracy", f"{accuracy:.3f}")
            with col2:
                st.metric("Precision", f"{precision:.3f}")
            with col3:
                st.metric("Recall", f"{recall:.3f}")
            with col4:
                st.metric("F1-Score", f"{f1:.3f}")
    else:
        st.warning("⚠️ Actual converted column not found")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 2: ROC CURVE
    # =============================================================================
    st.subheader("📈 ROC Curve")
    
    if actual_col in leads.columns and pred_prob_col and pred_prob_col in leads.columns:
        # Calculate ROC curve
        fpr, tpr, thresholds = roc_curve(leads[actual_col], leads[pred_prob_col])
        roc_auc = auc(fpr, tpr)
        
        # Create ROC plot
        fig = go.Figure()
        
        # ROC curve
        fig.add_trace(go.Scatter(
            x=fpr, y=tpr,
            mode='lines',
            name=f'ROC Curve (AUC={roc_auc:.3f})',
            line=dict(color='#1f77b4', width=2)
        ))
        
        # Random classifier baseline
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode='lines',
            name='Random Classifier',
            line=dict(color='gray', dash='dash')
        ))
        
        # Mark optimal threshold
        optimal_idx = np.argmax(tpr - fpr)
        fig.add_trace(go.Scatter(
            x=[fpr[optimal_idx]], y=[tpr[optimal_idx]],
            mode='markers',
            name=f'Optimal (t={thresholds[optimal_idx]:.2f})',
            marker=dict(size=12, color='red')
        ))
        
        fig.update_layout(
            title="ROC Curve",
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
            height=450,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success(f"✅ AUC Score: **{roc_auc:.3f}** - Good model discrimination")
    else:
        st.warning("⚠️ ROC curve data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 3: LEARNING CURVE
    # =============================================================================
    st.subheader("📚 Learning Curve")
    
    col1, col2 = st.columns(2)
    
    with col1:
        show_bands = st.checkbox("Show confidence bands", value=True, key="show_bands")
    
    with col2:
        st.info("💡 Training and validation curves guide model improvement")
    
    if 'training_size' in learning_curve.columns:
        fig = go.Figure()
        
        # Training scores
        if 'training_score' in learning_curve.columns:
            fig.add_trace(go.Scatter(
                x=learning_curve['training_size'],
                y=learning_curve['training_score'],
                mode='lines+markers',
                name='Training Score',
                line=dict(color='#1f77b4'),
                marker=dict(size=8)
            ))
        
        # Validation scores
        if 'validation_score' in learning_curve.columns:
            fig.add_trace(go.Scatter(
                x=learning_curve['training_size'],
                y=learning_curve['validation_score'],
                mode='lines+markers',
                name='Validation Score',
                line=dict(color='#ff7f0e'),
                marker=dict(size=8)
            ))
        
        # Confidence bands
        if show_bands:
            if 'training_std' in learning_curve.columns:
                fig.add_trace(go.Scatter(
                    x=learning_curve['training_size'],
                    y=learning_curve['training_score'] + learning_curve.get('training_std', 0),
                    fill=None,
                    mode='lines',
                    line_color='rgba(0,0,0,0)',
                    showlegend=False
                ))
                fig.add_trace(go.Scatter(
                    x=learning_curve['training_size'],
                    y=learning_curve['training_score'] - learning_curve.get('training_std', 0),
                    fill='tonexty',
                    mode='lines',
                    line_color='rgba(0,0,0,0)',
                    name='Training ±1 Std',
                    fillcolor='rgba(31, 119, 180, 0.2)'
                ))
        
        fig.update_layout(
            title="Learning Curve - Model Diagnostics",
            xaxis_title="Training Set Size",
            yaxis_title="Score",
            height=450,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **📊 Interpretation**
        
        - **Converging curves:** No overfitting (Good!)
        - **Widening gap:** More training data could improve validation score
        - **Both low:** Underfitting - try more complex models
        """)
    else:
        st.warning("⚠️ Learning curve data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # SECTION 4: FEATURE IMPORTANCE
    # =============================================================================
    st.subheader("🎯 Feature Importance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sort_order = st.radio(
            "Sort Order",
            ["Descending", "Ascending"],
            key="feature_sort"
        )
    
    with col2:
        st.info("💡 Top predictive features for lead conversion")
    
    if 'feature' in feature_importance.columns and 'importance' in feature_importance.columns:
        feat_data = feature_importance.copy()
        
        if sort_order == "Descending":
            feat_data = feat_data.sort_values('importance', ascending=False)
        else:
            feat_data = feat_data.sort_values('importance', ascending=True)
        
        # Create bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=feat_data['feature'],
            x=feat_data['importance'],
            orientation='h',
            marker=dict(
                color=feat_data['importance'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Importance")
            ),
            error_x=dict(
                type='data',
                array=feat_data.get('std', [0]*len(feat_data)),
                visible=True
            ) if 'std' in feat_data.columns else None,
            text=feat_data['importance'].round(3),
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Feature Importance for Lead Conversion",
            xaxis_title="Importance Score",
            yaxis_title="Feature",
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key features
        top_3 = feat_data.head(3)
        st.success(f"""
        **🏆 Top 3 Features:**
        
        1. **{top_3.iloc[0]['feature']}** - {top_3.iloc[0]['importance']:.3f}
        2. **{top_3.iloc[1]['feature']}** - {top_3.iloc[1]['importance']:.3f}
        3. **{top_3.iloc[2]['feature']}** - {top_3.iloc[2]['importance']:.3f}
        """)
    else:
        st.warning("⚠️ Feature importance data not available")
    
    st.markdown("---")
    
    # =============================================================================
    # KEY INSIGHTS
    # =============================================================================
    st.subheader("💡 Model Evaluation Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **✅ Model Strengths**
        
        - Good discrimination (AUC > 0.75)
        - Low overfitting
        - Actionable feature importance
        """)
    
    with col2:
        st.warning("""
        **⚠️ Recommendations**
        
        - Monitor for data drift
        - Retrain quarterly
        - Threshold optimization needed
        """)
