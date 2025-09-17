"""
Statistical Data Visualization System
A comprehensive web application for uploading and visualizing statistical data
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from scipy import stats
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'statistical-visualization-system'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data_file(filepath):
    """Load data from various file formats"""
    try:
        file_ext = filepath.rsplit('.', 1)[1].lower()
        
        if file_ext == 'csv':
            return pd.read_csv(filepath)
        elif file_ext in ['xlsx', 'xls']:
            return pd.read_excel(filepath)
        elif file_ext == 'json':
            return pd.read_json(filepath)
        elif file_ext == 'txt':
            # Try to read as CSV with different separators
            try:
                return pd.read_csv(filepath, sep='\t')
            except:
                return pd.read_csv(filepath, sep=' ')
    except Exception as e:
        raise ValueError(f"Error loading file: {str(e)}")

def get_data_characteristics(df):
    """Extract comprehensive characteristics from the dataset"""
    characteristics = {
        'basic_info': {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'data_types': df.dtypes.apply(str).to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum()
        },
        'missing_data': {
            'missing_counts': df.isnull().sum().to_dict(),
            'missing_percentages': (df.isnull().sum() / len(df) * 100).round(2).to_dict()
        },
        'numerical_stats': {},
        'categorical_stats': {}
    }
    
    # Numerical columns analysis
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        characteristics['numerical_stats'][col] = {
            'mean': float(df[col].mean()) if not df[col].isna().all() else None,
            'median': float(df[col].median()) if not df[col].isna().all() else None,
            'std': float(df[col].std()) if not df[col].isna().all() else None,
            'min': float(df[col].min()) if not df[col].isna().all() else None,
            'max': float(df[col].max()) if not df[col].isna().all() else None,
            'q25': float(df[col].quantile(0.25)) if not df[col].isna().all() else None,
            'q75': float(df[col].quantile(0.75)) if not df[col].isna().all() else None,
            'skewness': float(df[col].skew()) if not df[col].isna().all() else None,
            'kurtosis': float(df[col].kurtosis()) if not df[col].isna().all() else None
        }
    
    # Categorical columns analysis
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        characteristics['categorical_stats'][col] = {
            'unique_values': int(df[col].nunique()),
            'most_frequent': str(value_counts.index[0]) if len(value_counts) > 0 else None,
            'most_frequent_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else None,
            'value_counts': value_counts.head(10).to_dict()
        }
    
    return characteristics

def create_visualizations(df, characteristics):
    """Create various visualizations based on data characteristics"""
    visualizations = {}
    
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    # 1. Summary Statistics Visualization
    if len(numerical_cols) > 0:
        fig_summary = go.Figure()
        for col in numerical_cols[:5]:  # Limit to first 5 numerical columns
            stats_data = characteristics['numerical_stats'][col]
            fig_summary.add_trace(go.Bar(
                name=col,
                x=['Mean', 'Median', 'Std', 'Min', 'Max'],
                y=[stats_data['mean'], stats_data['median'], stats_data['std'], 
                   stats_data['min'], stats_data['max']]
            ))
        
        fig_summary.update_layout(
            title='Summary Statistics Comparison',
            xaxis_title='Statistical Measures',
            yaxis_title='Values',
            barmode='group'
        )
        visualizations['summary_stats'] = json.dumps(fig_summary, cls=PlotlyJSONEncoder)
    
    # 2. Distribution Plots
    if len(numerical_cols) > 0:
        fig_dist = go.Figure()
        for col in numerical_cols[:3]:  # First 3 numerical columns
            fig_dist.add_trace(go.Histogram(
                x=df[col].dropna(),
                name=f'{col} Distribution',
                opacity=0.7
            ))
        
        fig_dist.update_layout(
            title='Data Distribution Analysis',
            xaxis_title='Values',
            yaxis_title='Frequency',
            barmode='overlay'
        )
        visualizations['distributions'] = json.dumps(fig_dist, cls=PlotlyJSONEncoder)
    
    # 3. Correlation Heatmap
    if len(numerical_cols) > 1:
        corr_matrix = df[numerical_cols].corr()
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0
        ))
        
        fig_corr.update_layout(
            title='Correlation Matrix',
            xaxis_title='Variables',
            yaxis_title='Variables'
        )
        visualizations['correlation'] = json.dumps(fig_corr, cls=PlotlyJSONEncoder)
    
    # 4. Box Plots for Outlier Detection
    if len(numerical_cols) > 0:
        fig_box = go.Figure()
        for col in numerical_cols[:4]:  # First 4 numerical columns
            fig_box.add_trace(go.Box(
                y=df[col].dropna(),
                name=col,
                boxpoints='outliers'
            ))
        
        fig_box.update_layout(
            title='Box Plots for Outlier Detection',
            yaxis_title='Values'
        )
        visualizations['boxplots'] = json.dumps(fig_box, cls=PlotlyJSONEncoder)
    
    # 5. Categorical Data Visualization
    if len(categorical_cols) > 0:
        col = categorical_cols[0]  # First categorical column
        value_counts = df[col].value_counts().head(10)
        
        fig_cat = go.Figure(data=[
            go.Bar(x=value_counts.index, y=value_counts.values)
        ])
        
        fig_cat.update_layout(
            title=f'Top Categories in {col}',
            xaxis_title=col,
            yaxis_title='Count'
        )
        visualizations['categorical'] = json.dumps(fig_cat, cls=PlotlyJSONEncoder)
    
    # 6. Scatter Plot Matrix (if we have multiple numerical columns)
    if len(numerical_cols) >= 2:
        cols_for_scatter = numerical_cols[:3]  # Max 3 columns for readability
        fig_scatter = px.scatter_matrix(
            df[cols_for_scatter].dropna(),
            dimensions=cols_for_scatter,
            title="Scatter Plot Matrix"
        )
        visualizations['scatter_matrix'] = json.dumps(fig_scatter, cls=PlotlyJSONEncoder)
    
    return visualizations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Load and analyze the data
            df = load_data_file(filepath)
            characteristics = get_data_characteristics(df)
            visualizations = create_visualizations(df, characteristics)
            
            # Clean up the uploaded file
            os.remove(filepath)
            
            return render_template('results.html', 
                                 characteristics=characteristics,
                                 visualizations=visualizations,
                                 filename=filename)
        
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            if os.path.exists(filepath):
                os.remove(filepath)
            return redirect(url_for('index'))
    
    flash('Invalid file type. Please upload CSV, Excel, JSON, or TXT files.')
    return redirect(url_for('index'))

@app.route('/demo')
def demo():
    """Generate demo data for testing"""
    # Create sample dataset
    np.random.seed(42)
    data = {
        'Sales': np.random.normal(1000, 200, 100),
        'Marketing_Spend': np.random.normal(500, 100, 100),
        'Customer_Satisfaction': np.random.uniform(1, 5, 100),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'Product_Category': np.random.choice(['A', 'B', 'C'], 100)
    }
    df = pd.DataFrame(data)
    
    # Add some missing values for demonstration
    df.loc[df.sample(10).index, 'Customer_Satisfaction'] = np.nan
    
    characteristics = get_data_characteristics(df)
    visualizations = create_visualizations(df, characteristics)
    
    return render_template('results.html', 
                         characteristics=characteristics,
                         visualizations=visualizations,
                         filename='demo_data.csv')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)