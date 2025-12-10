# Data Folder

Place all CSV files in this directory.

## Required Files

1. **campaign_performance.csv**
   - Daily marketing campaign metrics
   - Columns: date, channel, region, impressions, clicks, conversions, spend, revenue, CTR, CPA, ROAS, campaign_type
   - Records: ~5,858

2. **customer_data.csv**
   - Customer demographics and behavior
   - Columns: customer_id, age, income, segment, lifetime_value, purchases, satisfaction, churn, engagement
   - Records: ~5,000

3. **product_sales.csv**
   - Hierarchical product sales data
   - Columns: category, subcategory, product, sales, units, profit_margin, region, quarter
   - Records: ~1,440

4. **lead_scoring_results.csv**
   - ML model lead predictions
   - Columns: lead_id, actual_converted, predicted_probability, predicted_class, feature1, feature2, ...
   - Records: ~2,000

5. **feature_importance.csv**
   - Feature importance from lead scoring model
   - Columns: feature, importance, std

6. **learning_curve.csv**
   - Training/validation curves
   - Columns: training_size, training_score, validation_score, training_std, validation_std

7. **geographic_data.csv**
   - State-level performance metrics
   - Columns: state, latitude, longitude, customers, revenue, market_penetration, satisfaction, yoy_growth
   - Records: ~15

8. **channel_attribution.csv**
   - Attribution model comparison
   - Columns: channel, first_touch, last_touch, linear, time_decay, position_based

9. **funnel_data.csv**
   - Marketing funnel stages
   - Columns: stage, visitors, conversions (or conversion_rate)
   - Expected stages: Awareness, Interest, Consideration, Evaluation, Decision, Purchase

10. **customer_journey.csv**
    - Multi-touchpoint customer journeys
    - Columns: journey_id, touchpoint_sequence, conversions (for Sankey)

11. **correlation_matrix.csv**
    - Pre-computed correlation matrix
    - Index: Metric names
    - Columns: Metric names
    - Values: Correlation coefficients (-1 to 1)

## Download Instructions

If data is provided in a different format:
1. Download files from the source
2. Convert to CSV format if necessary
3. Place all files in this `data/` directory
4. Ensure column names match those expected by the dashboard

## Testing

After adding files, run:
```bash
streamlit run app.py
```

The data loader will automatically find and load all CSV files in this directory.

## Notes

- All CSV files should be in **UTF-8 encoding**
- Column names are **case-sensitive**
- Date columns should be in ISO format (YYYY-MM-DD)
- Ensure no missing values in critical columns
- Large files may impact performance on free Streamlit Cloud tier

## Data Privacy

This data folder should NOT be committed to GitHub (see `.gitignore`).
For Streamlit Cloud deployment, upload data through the platform's interface or use a separate data service.
