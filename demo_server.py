"""
Simplified Statistical Data Visualization System
A demonstration version using minimal dependencies
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import webbrowser
import threading
import time

class StatisticalServer(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=None, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_file('demo_index.html', 'text/html')
        elif self.path == '/demo':
            self.serve_file('demo_results.html', 'text/html')
        elif self.path.endswith('.css'):
            self.serve_file(self.path[1:], 'text/css')
        elif self.path.endswith('.js'):
            self.serve_file(self.path[1:], 'application/javascript')
        else:
            self.send_error(404)
    
    def serve_file(self, filename, content_type):
        """Serve a file with proper content type"""
        try:
            if filename.startswith('demo_'):
                # These are special demo files we'll generate
                content = self.generate_demo_content(filename)
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                # Regular file serving
                with open(filename, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)
    
    def generate_demo_content(self, filename):
        """Generate demo HTML content"""
        if filename == 'demo_index.html':
            return self.get_demo_index()
        elif filename == 'demo_results.html':
            return self.get_demo_results()
        return ""
    
    def get_demo_index(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Statistical Data Visualization System - Demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .card { border: none; border-radius: 15px; box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); }
        .btn-primary { border-radius: 10px; font-weight: 500; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-chart-line me-2"></i>
                Statistical Analytics System (Demo)
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/demo">
                    <i class="fas fa-play me-1"></i>
                    View Demo Results
                </a>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="text-center mb-5">
                    <h1 class="display-4">
                        <i class="fas fa-chart-bar text-primary me-3"></i>
                        Demo Mode
                    </h1>
                    <p class="lead text-muted">
                        This is a demonstration of the Statistical Data Visualization System.
                        Click below to see sample analysis results.
                    </p>
                </div>

                <div class="card shadow-lg">
                    <div class="card-body p-5 text-center">
                        <h3 class="mb-4">Sample Dataset Analysis</h3>
                        <p class="mb-4">Experience the power of comprehensive statistical analysis with our sample business dataset.</p>
                        
                        <a href="/demo" class="btn btn-primary btn-lg">
                            <i class="fas fa-chart-bar me-2"></i>
                            View Sample Analysis
                        </a>
                    </div>
                </div>

                <div class="row mt-5">
                    <div class="col-md-4">
                        <div class="text-center p-3">
                            <i class="fas fa-chart-pie fa-3x text-primary mb-3"></i>
                            <h5>Multiple Chart Types</h5>
                            <p class="text-muted">Interactive visualizations including histograms, scatter plots, and correlation matrices</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center p-3">
                            <i class="fas fa-calculator fa-3x text-success mb-3"></i>
                            <h5>Statistical Analysis</h5>
                            <p class="text-muted">Comprehensive statistics including descriptive measures and data quality assessment</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center p-3">
                            <i class="fas fa-upload fa-3x text-info mb-3"></i>
                            <h5>File Upload Support</h5>
                            <p class="text-muted">Support for CSV, Excel, JSON, and TXT files with automatic data type detection</p>
                        </div>
                    </div>
                </div>

                <div class="alert alert-info mt-4">
                    <h5><i class="fas fa-info-circle me-2"></i>Demo Note</h5>
                    <p class="mb-0">This is a demonstration version. The full system includes file upload capabilities and real-time data processing.</p>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

    def get_demo_results(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo Results - Statistical Analytics System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { background-color: #f8f9fa; }
        .card { border: none; border-radius: 15px; box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); }
        .js-plotly-plot { width: 100% !important; height: 400px !important; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-chart-line me-2"></i>
                Statistical Analytics System
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/">
                    <i class="fas fa-home me-1"></i>
                    Home
                </a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="fas fa-chart-bar text-primary me-2"></i>
                        Sample Analysis Results
                    </h1>
                    <span class="badge bg-primary fs-6">sales_data_sample.csv</span>
                </div>
            </div>
        </div>

        <!-- Dataset Overview -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-info-circle me-2"></i>
                            Dataset Overview
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-3">
                                <div class="text-center p-3 bg-light rounded">
                                    <h3 class="text-primary">100</h3>
                                    <small class="text-muted">Rows</small>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center p-3 bg-light rounded">
                                    <h3 class="text-success">5</h3>
                                    <small class="text-muted">Columns</small>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center p-3 bg-light rounded">
                                    <h3 class="text-info">12.4</h3>
                                    <small class="text-muted">KB Memory</small>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center p-3 bg-light rounded">
                                    <h3 class="text-warning">5</h3>
                                    <small class="text-muted">Total Features</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Visualizations -->
        <div class="row">
            <div class="col-12 mb-4">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-chart-bar me-2"></i>
                            Sales Performance Analysis
                        </h5>
                    </div>
                    <div class="card-body">
                        <div id="sales_chart"></div>
                    </div>
                </div>
            </div>

            <div class="col-lg-6 mb-4">
                <div class="card h-100">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-chart-area me-2"></i>
                            Revenue Distribution
                        </h5>
                    </div>
                    <div class="card-body">
                        <div id="revenue_chart"></div>
                    </div>
                </div>
            </div>

            <div class="col-lg-6 mb-4">
                <div class="card h-100">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-project-diagram me-2"></i>
                            Regional Performance
                        </h5>
                    </div>
                    <div class="card-body">
                        <div id="regional_chart"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Statistics Tables -->
        <div class="row">
            <div class="col-lg-6 mb-4">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-calculator me-2"></i>
                            Key Statistics
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover">
                                <thead class="table-dark">
                                    <tr>
                                        <th>Metric</th>
                                        <th>Sales</th>
                                        <th>Marketing</th>
                                        <th>Satisfaction</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><strong>Mean</strong></td>
                                        <td>1000.15</td>
                                        <td>499.87</td>
                                        <td>3.01</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Median</strong></td>
                                        <td>998.32</td>
                                        <td>501.23</td>
                                        <td>3.05</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Std Dev</strong></td>
                                        <td>199.78</td>
                                        <td>99.45</td>
                                        <td>1.15</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Min</strong></td>
                                        <td>567.23</td>
                                        <td>298.76</td>
                                        <td>1.02</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Max</strong></td>
                                        <td>1456.78</td>
                                        <td>697.89</td>
                                        <td>4.98</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-6 mb-4">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            Data Quality Assessment
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead class="table-dark">
                                    <tr>
                                        <th>Column</th>
                                        <th>Missing %</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><strong>Sales</strong></td>
                                        <td>0.0%</td>
                                        <td><span class="badge bg-success">Complete</span></td>
                                    </tr>
                                    <tr>
                                        <td><strong>Marketing</strong></td>
                                        <td>0.0%</td>
                                        <td><span class="badge bg-success">Complete</span></td>
                                    </tr>
                                    <tr>
                                        <td><strong>Satisfaction</strong></td>
                                        <td>10.0%</td>
                                        <td><span class="badge bg-warning">Minor Missing</span></td>
                                    </tr>
                                    <tr>
                                        <td><strong>Region</strong></td>
                                        <td>0.0%</td>
                                        <td><span class="badge bg-success">Complete</span></td>
                                    </tr>
                                    <tr>
                                        <td><strong>Category</strong></td>
                                        <td>0.0%</td>
                                        <td><span class="badge bg-success">Complete</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="alert alert-success">
            <h5><i class="fas fa-check-circle me-2"></i>Analysis Complete</h5>
            <p class="mb-0">Your dataset has been successfully analyzed. The results show good data quality with minimal missing values and clear patterns in sales performance across regions.</p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Sample Sales Performance Chart
        var salesData = {
            data: [{
                x: ['North', 'South', 'East', 'West'],
                y: [1250, 980, 1150, 890],
                type: 'bar',
                marker: {
                    color: ['#0d6efd', '#198754', '#dc3545', '#ffc107']
                }
            }],
            layout: {
                title: 'Sales by Region',
                xaxis: { title: 'Region' },
                yaxis: { title: 'Sales Volume' }
            }
        };
        Plotly.newPlot('sales_chart', salesData.data, salesData.layout);

        // Revenue Distribution Chart
        var revenueData = {
            data: [{
                x: [800, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300],
                type: 'histogram',
                marker: { color: '#198754', opacity: 0.7 }
            }],
            layout: {
                title: 'Revenue Distribution',
                xaxis: { title: 'Revenue ($)' },
                yaxis: { title: 'Frequency' }
            }
        };
        Plotly.newPlot('revenue_chart', revenueData.data, revenueData.layout);

        // Regional Performance Pie Chart
        var regionalData = {
            data: [{
                values: [1250, 980, 1150, 890],
                labels: ['North', 'South', 'East', 'West'],
                type: 'pie',
                marker: {
                    colors: ['#0d6efd', '#198754', '#dc3545', '#ffc107']
                }
            }],
            layout: {
                title: 'Market Share by Region'
            }
        };
        Plotly.newPlot('regional_chart', regionalData.data, regionalData.layout);

        // Make plots responsive
        window.addEventListener('resize', function() {
            Plotly.Plots.resize('sales_chart');
            Plotly.Plots.resize('revenue_chart');
            Plotly.Plots.resize('regional_chart');
        });
    </script>
</body>
</html>"""

def start_server():
    """Start the demo server"""
    port = 8000
    server = HTTPServer(('localhost', port), StatisticalServer)
    print(f"Demo server starting at http://localhost:{port}")
    print("Opening browser...")
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(1)
        webbrowser.open(f'http://localhost:{port}')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()

if __name__ == "__main__":
    start_server()