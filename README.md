# Statistical Data Visualization System

A comprehensive web-based application for uploading, analyzing, and visualizing statistical data. This system provides detailed insights into your datasets with interactive charts, statistical analysis, and data quality assessment.

## 🚀 Features

### 📊 Comprehensive Data Analysis
- **Automatic Data Type Detection**: Identifies numerical and categorical variables
- **Statistical Summary**: Mean, median, standard deviation, skewness, kurtosis, and more
- **Missing Data Analysis**: Identifies and quantifies missing values
- **Outlier Detection**: Box plots for identifying data anomalies

### 📈 Multiple Visualization Types
- **Distribution Analysis**: Histograms for understanding data spread
- **Correlation Matrix**: Heatmap showing relationships between variables
- **Box Plots**: Outlier detection and quartile analysis
- **Scatter Plot Matrix**: Pairwise relationships between numerical variables
- **Categorical Analysis**: Bar charts for categorical data exploration
- **Summary Statistics**: Comparative bar charts of key metrics

### 🎯 Interactive Features
- **File Upload Support**: CSV, Excel (.xlsx, .xls), JSON, and TXT formats
- **Real-time Processing**: Instant analysis upon file upload
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Demo Mode**: Built-in sample data for testing

### 🔍 Data Quality Assessment
- **Missing Value Tracking**: Percentage and count of missing data
- **Data Type Validation**: Automatic detection and validation
- **Memory Usage Analysis**: Dataset size and memory consumption
- **Statistical Health Check**: Skewness and kurtosis indicators

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/samthosiac/First-Year-Comp-E-Business-Analytics-Projects.git
   cd First-Year-Comp-E-Business-Analytics-Projects
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`

## 📝 Usage Guide

### Uploading Data
1. Navigate to the home page
2. Click "Choose File" and select your dataset
3. Supported formats: CSV, Excel (.xlsx, .xls), JSON, TXT
4. Click "Analyze Data" to process your file

### Understanding Results

#### Dataset Overview
- **Rows**: Number of observations in your dataset
- **Columns**: Number of variables/features
- **Memory Usage**: Storage requirements in KB
- **Total Columns**: Sum of numerical and categorical columns

#### Visualizations
- **Summary Statistics**: Comparative view of key statistical measures
- **Data Distributions**: Frequency distribution of numerical variables
- **Correlation Matrix**: Color-coded correlation coefficients
- **Outlier Detection**: Box plots showing data spread and outliers
- **Categorical Analysis**: Frequency of categorical values
- **Scatter Plot Matrix**: Pairwise relationships (for numerical data)

#### Statistical Tables
- **Numerical Statistics**: Detailed metrics for numerical columns
- **Categorical Statistics**: Unique values and frequency for categorical columns
- **Missing Data Analysis**: Complete overview of data completeness

### Demo Mode
Try the system with sample data by clicking the "Demo" button in the navigation bar.

## 📁 Project Structure

```
First-Year-Comp-E-Business-Analytics-Projects/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Upload page
│   └── results.html      # Results page
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/               # JavaScript files (if needed)
├── sample_data/          # Example datasets
│   ├── sales_data.csv    # Sample sales data
│   └── employee_data.csv # Sample employee data
└── uploads/              # Temporary upload directory
```

## 🔧 Technical Details

### Backend Technologies
- **Flask**: Web framework for Python
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib & Seaborn**: Statistical plotting
- **Plotly**: Interactive visualizations
- **SciPy**: Scientific computing and statistics
- **Scikit-learn**: Machine learning utilities

### Frontend Technologies
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome**: Icon library
- **Plotly.js**: Interactive charting library
- **HTML5 & CSS3**: Modern web standards

### Key Features Implementation

#### Data Processing Pipeline
1. **File Upload**: Secure file handling with validation
2. **Data Loading**: Multi-format support with error handling
3. **Analysis Engine**: Comprehensive statistical analysis
4. **Visualization Generator**: Dynamic chart creation
5. **Results Rendering**: Interactive web-based display

#### Statistical Analysis
- **Descriptive Statistics**: Central tendency and dispersion measures
- **Distribution Analysis**: Shape and normality assessment
- **Correlation Analysis**: Linear relationship detection
- **Missing Data Assessment**: Data quality evaluation
- **Outlier Detection**: Anomaly identification

## 🎯 Use Cases

### Business Analytics
- Sales performance analysis
- Customer behavior insights
- Market research data exploration
- Financial data assessment

### Academic Research
- Dataset exploration and validation
- Statistical hypothesis testing preparation
- Research data quality assessment
- Preliminary data analysis

### Data Science Projects
- Exploratory data analysis (EDA)
- Feature engineering preparation
- Data preprocessing insights
- Model input validation

## 📊 Sample Data

The project includes sample datasets for testing:

### Sales Data (`sample_data/sales_data.csv`)
- Product performance metrics
- Regional sales analysis
- Customer ratings and revenue data
- Marketing spend effectiveness

### Employee Data (`sample_data/employee_data.csv`)
- HR analytics dataset
- Salary and performance metrics
- Demographic and educational data
- Department-wise analysis

## 🔒 Security Features

- **File Type Validation**: Only allows specified file formats
- **File Size Limits**: Maximum 16MB upload size
- **Secure File Handling**: Prevents malicious file uploads
- **Temporary Storage**: Automatic cleanup of uploaded files
- **Input Sanitization**: Protection against code injection

## 🚀 Future Enhancements

- **Advanced Statistical Tests**: Hypothesis testing capabilities
- **Machine Learning Integration**: Automated model suggestions
- **Export Functionality**: Download results as PDF/Excel
- **Database Integration**: Persistent data storage
- **User Authentication**: Multi-user support
- **API Endpoints**: Programmatic access to analysis features

## 🤝 Contributing

This project is part of first-year Computer Engineering business analytics skill development. Contributions, suggestions, and feedback are welcome!

## 📄 License

This project is developed for educational purposes as part of internship preparation.

## 📞 Support

For questions or issues, please create an issue in the GitHub repository.

---

**Built with ❤️ for data enthusiasts and business analysts**
