# NovaMart Marketing Analytics Dashboard

A comprehensive interactive Streamlit dashboard for analyzing marketing performance, customer behavior, product sales, and ML model evaluation. Built for NovaMart, a rapidly growing omnichannel retail company across India.

## 🎯 Overview

This dashboard provides marketing leadership with a powerful tool to explore 11 interconnected datasets spanning:
- Campaign performance across multiple channels and regions
- Customer demographics, behavior, and lifetime value
- Product sales hierarchies and profitability
- Geographic market penetration and regional performance
- Marketing funnel and attribution models
- Lead scoring ML model evaluation and diagnostics

**Live Demo:** [Streamlit Cloud Link - Add your deployment URL here]

## ✨ Features

### 📊 7 Comprehensive Dashboard Pages

1. **🏠 Executive Overview**
   - Key performance indicator cards (Revenue, Conversions, ROAS, Ad Spend)
   - Real-time revenue trend visualization with temporal aggregation
   - Channel performance comparison with metric selection
   - Interactive filters for deep analysis

2. **📈 Campaign Analytics**
   - Regional performance comparison by quarter
   - Campaign type contribution stacked bar charts
   - Cumulative conversions area charts with regional filters
   - Daily performance calendar heatmap with metric selection

3. **👥 Customer Insights**
   - Customer age distribution histogram with adjustable bins
   - Lifetime value distribution by segment (box plots)
   - Satisfaction score distribution by NPS category (violin plots)
   - Income vs. LTV correlation scatter plots
   - Customer segmentation sunburst hierarchy

4. **📦 Product Performance**
   - Interactive product hierarchy treemap (drill-down enabled)
   - Category performance metrics comparison
   - Regional product performance analysis
   - Quarterly sales trend visualization

5. **🗺️ Geographic Analysis**
   - State-wise performance metrics ranking
   - Geographic revenue distribution pie chart
   - Multi-metric geographic scatter plots
   - Satisfaction and market penetration analysis

6. **🎯 Attribution & Funnel**
   - Marketing conversion funnel with stage-to-stage rates
   - Attribution model comparison (First-touch, Last-touch, Linear, etc.)
   - Metric correlation heatmap with diverging color scales
   - Donut charts for multi-model attribution view

7. **🤖 ML Model Evaluation**
   - Confusion matrix heatmap with adjustable classification threshold
   - ROC curve with AUC score and optimal threshold marking
   - Learning curves showing training/validation dynamics
   - Feature importance bar charts with error bars
   - Comprehensive model evaluation metrics (Accuracy, Precision, Recall, F1)

### 🎨 Interactive Features

- **Dropdown & Multi-Select Filters:** Channel, Region, Year, Segment, Attribution Model selection
- **Dynamic Thresholds:** Adjust classification thresholds for ML model evaluation
- **Temporal Aggregation:** Toggle between Daily, Weekly, Monthly views
- **Metric Selection:** Switch between Revenue, Conversions, ROAS on demand
- **Hover Information:** Rich tooltips with detailed metrics on all charts
- **Responsive Design:** Mobile-friendly layout with column-based responsive grids

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for version control and GitHub deployment)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/novamart-analytics.git
   cd novamart-analytics
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare your data**
   - Place all CSV files in a `data/` folder in the project root:
     ```
     data/
     ├── campaign_performance.csv
     ├── customer_data.csv
     ├── product_sales.csv
     ├── lead_scoring_results.csv
     ├── feature_importance.csv
     ├── learning_curve.csv
     ├── geographic_data.csv
     ├── channel_attribution.csv
     ├── funnel_data.csv
     ├── customer_journey.csv
     └── correlation_matrix.csv
     ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The dashboard will open in your default browser at `http://localhost:8501`

## 📊 Dataset Overview

| File | Description | Records |
|------|-------------|---------|
| `campaign_performance.csv` | Daily marketing metrics: impressions, clicks, conversions, spend, revenue, CTR, CPA, ROAS | 5,858 |
| `customer_data.csv` | Customer demographics and behavior: age, income, LTV, purchases, satisfaction | 5,000 |
| `product_sales.csv` | Hierarchical product sales by category, subcategory, product | 1,440 |
| `lead_scoring_results.csv` | ML model predictions for lead conversion | 2,000 |
| `feature_importance.csv` | Feature importance scores from lead scoring model | N/A |
| `learning_curve.csv` | Training/validation scores at different training set sizes | N/A |
| `geographic_data.csv` | State-level metrics: customers, revenue, market penetration, satisfaction | 15 |
| `channel_attribution.csv` | Attribution model comparison across channels | N/A |
| `funnel_data.csv` | Marketing funnel stages with conversion metrics | N/A |
| `customer_journey.csv` | Multi-touchpoint customer journeys | N/A |
| `correlation_matrix.csv` | Pre-computed correlation matrix for 10 key metrics | N/A |

## 🏗️ Project Structure

```
novamart-analytics/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore file
├── utils/
│   ├── __init__.py
│   ├── data_loader.py              # Data loading and preprocessing utilities
│   └── pages/
│       ├── __init__.py
│       ├── executive_overview.py   # Page 1: Executive Overview
│       ├── campaign_analytics.py   # Page 2: Campaign Analytics
│       ├── customer_insights.py    # Page 3: Customer Insights
│       ├── product_performance.py  # Page 4: Product Performance
│       ├── geographic_analysis.py  # Page 5: Geographic Analysis
│       ├── attribution_funnel.py   # Page 6: Attribution & Funnel
│       └── ml_model_evaluation.py  # Page 7: ML Model Evaluation
└── data/                           # Data folder (create this)
    ├── campaign_performance.csv
    ├── customer_data.csv
    ├── [... other CSV files ...]
    └── README.md
```

## 🌐 Deploying to Streamlit Cloud

### Prerequisites
- GitHub account with your repository
- Streamlit account (free at https://streamlit.io)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: NovaMart Marketing Analytics Dashboard"
   git branch -M main
   git remote add origin https://github.com/yourusername/novamart-analytics.git
   git push -u origin main
   ```

2. **Create Streamlit Cloud Deployment**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repository
   - Specify the main file: `app.py`
   - Click "Deploy"

3. **Configure Secrets** (if using sensitive data)
   - In Streamlit Cloud, go to Settings → Secrets
   - Add any API keys or credentials

4. **Your app is live!**
   - Access it via the URL provided by Streamlit Cloud
   - Share with stakeholders

### Typical Deployment URL
```
https://yourusername-novamart-analytics-appxyz.streamlit.app
```

## 📈 Key Business Insights

The dashboard reveals several important marketing insights:

- **Regional Performance:** West and South regions consistently outperform; Q4 shows significant festive season boost
- **Channel Efficiency:** Google Ads and Email drive highest revenue; LinkedIn shows quality over quantity
- **Customer Segments:** Premium segment has highest LTV; Budget segment shows upgrade potential
- **Product Mix:** Electronics dominates volume; Fashion shows highest profit margins
- **Geographic Opportunity:** Eastern states show lower penetration but strong growth potential
- **Model Performance:** Lead scoring model shows good discrimination (AUC > 0.75) with actionable features
- **Funnel Optimization:** Largest drop-off occurs at awareness-to-interest stage; focus efforts there

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend Framework** | Streamlit 1.28.0+ |
| **Data Processing** | Pandas 2.0.0+, NumPy 1.24.0+ |
| **Visualization** | Plotly 5.17.0+, Altair 5.0.0+ |
| **ML/Statistics** | Scikit-learn 1.3.0+, SciPy 1.10.0+ |
| **Plotting** | Matplotlib 3.7.0+, Seaborn 0.12.0+ |
| **Deployment** | Streamlit Cloud |
| **Version Control** | Git, GitHub |

## 📋 Features Implemented

### Visualization Types (20+ Charts)
- ✅ Horizontal bar charts (channel performance)
- ✅ Grouped bar charts (regional performance by quarter)
- ✅ Stacked bar charts (campaign type contribution)
- ✅ Line charts (revenue trends)
- ✅ Area charts (cumulative conversions)
- ✅ Histograms (age distribution)
- ✅ Box plots (LTV by segment)
- ✅ Violin plots (satisfaction distribution)
- ✅ Scatter plots (income vs. LTV)
- ✅ Bubble charts (channel performance matrix)
- ✅ Heatmaps (correlation matrix, calendar heatmap)
- ✅ Pie/Donut charts (attribution models)
- ✅ Treemaps (product hierarchy)
- ✅ Sunburst charts (customer segmentation)
- ✅ Funnel charts (conversion funnel)
- ✅ Confusion matrix heatmap
- ✅ ROC curves (model evaluation)
- ✅ Learning curves (model diagnostics)
- ✅ Feature importance bar charts

### Interactive Features
- ✅ Dropdown filters for channels, regions, years, metrics
- ✅ Multi-select filters for complex filtering
- ✅ Date range selectors
- ✅ Toggle switches for data views
- ✅ Threshold adjustment sliders
- ✅ Bin size controls
- ✅ Sort order controls
- ✅ Real-time metric calculations
- ✅ Responsive layout design
- ✅ Rich hover tooltips

### Code Quality
- ✅ Modular page-based architecture
- ✅ Streamlit `@st.cache_data` for performance optimization
- ✅ Comprehensive docstrings and comments
- ✅ Error handling for missing data
- ✅ Clean variable naming conventions
- ✅ Separated concerns (data loading, processing, visualization)

## 🔧 Configuration

### Custom Data Paths
If your data is in a different location, modify the data path in `utils/data_loader.py`:

```python
data_paths = [
    Path("your/custom/path"),
    Path(__file__).parent.parent / "data",
    # ... other paths
]
```

### Streamlit Configuration
Create a `.streamlit/config.toml` file for custom settings:

```toml
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true

[logger]
level = "info"
```

## 🐛 Troubleshooting

### Issue: "Data file not found"
**Solution:** Ensure all CSV files are in the `data/` folder and the path is correct in `data_loader.py`.

### Issue: "Module not found" errors
**Solution:** Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Slow performance
**Solution:** 
- Streamlit caches data automatically, but you can increase cache size in `.streamlit/config.toml`
- Reduce data size or aggregate before visualization
- Check your browser's resource usage

### Issue: Blank or missing charts
**Solution:**
- Check that required columns exist in your CSV files
- Verify column names match the code (case-sensitive)
- Check data types (dates should be datetime format)

## 📧 Support & Contact

For issues, questions, or feature requests:
- Open an issue on GitHub
- Contact: [your-email@example.com]
- Documentation: See individual page docstrings in code

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎓 Course Information

**Program:** Masters of AI in Business  
**Course:** Data Visualization  
**Assignment:** NovaMart Marketing Analytics Dashboard  
**Institution:** SP Jain School of Global Management  

## 👥 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Dataset provided by NovaMart Analytics Team
- Streamlit community for excellent documentation
- Plotly for interactive visualization library
- Scikit-learn for ML evaluation metrics

---

**Last Updated:** December 2024  
**Version:** 1.0.0  
**Status:** Production Ready ✅
