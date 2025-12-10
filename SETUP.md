# NovaMart Analytics - Setup & Deployment Guide

## Quick Start (Local Development)

### 1. Clone or Download the Repository
```bash
git clone https://github.com/yourusername/novamart-analytics.git
cd novamart-analytics
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Your Data
Create a `data/` folder in the project root and add all CSV files:
- campaign_performance.csv
- customer_data.csv
- product_sales.csv
- lead_scoring_results.csv
- feature_importance.csv
- learning_curve.csv
- geographic_data.csv
- channel_attribution.csv
- funnel_data.csv
- customer_journey.csv
- correlation_matrix.csv

### 5. Run the Dashboard
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## GitHub Preparation

### Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit: NovaMart Marketing Analytics Dashboard"
git branch -M main
```

### Add Remote Repository
```bash
git remote add origin https://github.com/yourusername/novamart-analytics.git
git push -u origin main
```

### Important: Add `.gitignore`
The project includes a `.gitignore` file. Ensure CSV data files are NOT committed:
```bash
git status  # Check before pushing
```

---

## Streamlit Cloud Deployment

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Create repository: `novamart-analytics`
3. Push your code (see GitHub Preparation above)

### Step 2: Deploy to Streamlit Cloud
1. Visit https://share.streamlit.io
2. Click "New app"
3. Select:
   - **GitHub account:** Your GitHub username
   - **Repository:** novamart-analytics
   - **Branch:** main
   - **Main file path:** app.py
4. Click "Deploy"

### Step 3: Configure Secrets (Optional)
If using API keys or sensitive data:
1. In Streamlit Cloud dashboard → Settings
2. Click "Secrets" tab
3. Add your secrets in TOML format:
```toml
[database]
api_key = "your_key_here"
```

### Step 4: Share Your Dashboard
- Your app URL will be: `https://yourusername-novamart-analytics-appXXX.streamlit.app`
- Share this link with stakeholders

---

## File Structure for GitHub

```
novamart-analytics/
├── .gitignore                      # Prevents committing data/secrets
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── app.py                         # Main application
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── SETUP.md                       # This file
├── utils/
│   ├── __init__.py
│   ├── data_loader.py
│   └── pages/
│       ├── __init__.py
│       ├── executive_overview.py
│       ├── campaign_analytics.py
│       ├── customer_insights.py
│       ├── product_performance.py
│       ├── geographic_analysis.py
│       ├── attribution_funnel.py
│       └── ml_model_evaluation.py
└── data/                          # DO NOT COMMIT - .gitignore handles this
    ├── campaign_performance.csv
    ├── customer_data.csv
    └── ... (other CSV files)
```

---

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Data not loading
- Check `data/` folder exists in project root
- Verify CSV file names match exactly (case-sensitive)
- Check CSV column names in code match your files

### Slow performance
- Streamlit caches data automatically via `@st.cache_data`
- For large datasets, consider aggregating before upload
- Increase Streamlit cache size in `.streamlit/config.toml`

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

---

## Update & Maintain

### Pulling Latest Changes
```bash
git pull origin main
pip install -r requirements.txt  # If dependencies changed
```

### Pushing Updates
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will auto-redeploy when you push to main branch.

---

## Performance Tips

1. **Data Loading:** Uses `@st.cache_data` for automatic caching
2. **Large Datasets:** Consider pre-aggregating data before visualization
3. **Memory:** Streamlit Cloud free tier has limits; optimize queries
4. **Images:** Cache large visualizations when possible

---

## Security Notes

- **Never commit `.env` files** with secrets
- **Use Streamlit Secrets** for API keys in production
- **Data Privacy:** Ensure compliance with data protection regulations
- **Update Dependencies:** Run `pip install --upgrade -r requirements.txt` regularly

---

## Support Resources

- Streamlit Docs: https://docs.streamlit.io
- Plotly Docs: https://plotly.com/python
- Pandas Docs: https://pandas.pydata.org
- Scikit-learn Docs: https://scikit-learn.org

---

**Happy Analyzing! 📊**
