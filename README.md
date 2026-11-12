
# AI Analytics Copilot

An interactive AI-assisted business analytics dashboard built using Python and Streamlit. It helps users explore business data, monitor performance, identify unusual transactions, and generate actionable business insights.

## Project Features

- CSV and Excel file upload
- Interactive business dashboard
- KPI cards for Sales, Profit, Quantity and Records
- Regional Sales Performance Analysis
- Product Sales Analysis
- Sales vs Profit Analysis
- Sales Trend Analysis
- Profitability Analysis
- Dashboard filters by Region and Product
- Automated Business Insights
- Ask Your Data – rule-based question answering
- ML-based Anomaly Detection using Isolation Forest
- Data Quality Report
- Business Recommendations
- Input validation and error handling

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- OpenPyXL

## Project Structure

```text
AI Analytics Copilot/
│
├── app.py
├── sample_data.csv
├── test_gemini.py
├── README.md
├── .gitignore
└── .venv/
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd "AI Analytics Copilot"
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install streamlit pandas numpy plotly openpyxl scikit-learn
```

## Run the Application

```bash
python -m streamlit run app.py
```

## How to Use

1. Launch the Streamlit application.
2. Upload a CSV or Excel business dataset.
3. Explore the KPI cards and interactive charts.
4. Apply Region and Product filters.
5. Review data quality and anomaly detection results.
6. Ask questions about your business data.
7. Review automated insights and business recommendations.

## Machine Learning

The project uses the Isolation Forest algorithm from Scikit-learn to identify unusual business records based on Sales, Profit and Quantity.

## Note

The current Ask Your Data feature uses rule-based question matching. Automated insights and business recommendations are rule-based. Anomaly detection uses a machine learning model.

## Author

Keshav Bajaj
