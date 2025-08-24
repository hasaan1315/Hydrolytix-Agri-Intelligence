"""
Hydrolytix Agri Dashboard - Clean, Modular Architecture
Main application entry point with clean styling and modular components.
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from datetime import datetime
import base64
 
# Import modular components
from utils.data_loader import DataLoader
from utils.formatters import Formatters
from components.layout import DashboardLayout
from components.comparison import YearComparison
from components.forecasting import Forecasting
from components.trend_analysis import TrendAnalysis
from components.export_reports import ExportReports

# Initialize data loader
data_loader = DataLoader("agri_analysis_punjab_clean.csv")

# Initialize comparison component
year_comparison = YearComparison(data_loader)

# Initialize forecasting component
forecasting = Forecasting(data_loader)

# Initialize trend analysis component
trend_analysis = TrendAnalysis(data_loader)

# Initialize export reports component
export_reports = ExportReports(data_loader)

# Create the app
app = dash.Dash(__name__, 
                external_stylesheets=[
                    "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
                    "/assets/base.css",
                    "/assets/components.css",
                    "/assets/layout.css"
                ],
                suppress_callback_exceptions=True)
app.title = "Hydrolytix • Agri Intelligence"

# Create layout
dashboard_layout = DashboardLayout(data_loader)
app.layout = dashboard_layout.create_layout()

# Tab switching callback
@app.callback(
    [Output("tab-content", "children"),
     Output("overview-tab", "className"),
     Output("comparison-tab", "className"),
     Output("forecasting-tab", "className"),
     Output("trend-analysis-tab", "className"),
     Output("export-reports-tab", "className")],
    [Input("overview-tab", "n_clicks"),
     Input("comparison-tab", "n_clicks"),
     Input("forecasting-tab", "n_clicks"),
     Input("trend-analysis-tab", "n_clicks"),
     Input("export-reports-tab", "n_clicks")],
    prevent_initial_call=True
)
def switch_tab(overview_clicks, comparison_clicks, forecasting_clicks, trend_analysis_clicks, export_reports_clicks):
    """Switch between tabs based on button clicks."""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return dashboard_layout._create_overview_layout(), "custom-tab active", "custom-tab", "custom-tab", "custom-tab", "custom-tab"
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "overview-tab":
        return dashboard_layout._create_overview_layout(), "custom-tab active", "custom-tab", "custom-tab", "custom-tab", "custom-tab"
    elif button_id == "comparison-tab":
        return dashboard_layout._create_comparison_layout(), "custom-tab", "custom-tab active", "custom-tab", "custom-tab", "custom-tab"
    elif button_id == "forecasting-tab":
        return dashboard_layout._create_forecasting_layout(), "custom-tab", "custom-tab", "custom-tab active", "custom-tab", "custom-tab"
    elif button_id == "trend-analysis-tab":
        return dashboard_layout._create_trend_analysis_layout(), "custom-tab", "custom-tab", "custom-tab", "custom-tab active", "custom-tab"
    elif button_id == "export-reports-tab":
        return dashboard_layout._create_export_reports_layout(), "custom-tab", "custom-tab", "custom-tab", "custom-tab", "custom-tab active"
    
    return dashboard_layout._create_overview_layout(), "custom-tab active", "custom-tab", "custom-tab", "custom-tab", "custom-tab"

# Existing Callbacks
@app.callback(
    [
        Output("kpi-area", "children"),
        Output("kpi-area-sub", "children"),
        Output("kpi-burned", "children"),
        Output("kpi-burned-sub", "children"),
        Output("kpi-diff", "children"),
        Output("kpi-diff-sub", "children"),
        Output("kpi-pct", "children"),
        Output("kpi-pct-sub", "children"),
        Output("donut-fig", "figure"),
        Output("donut-title", "children"),
        Output("trend-fig", "figure"),
        Output("trend-title", "children"),
    ],
    [Input("overview-season-dd", "value"), Input("overview-year-dd", "value")],
)
def update_dashboard(season, year):
    """Update dashboard based on filter selections."""
    
    # Get filtered data
    filtered_df = data_loader.filter_data(season, year)
    
    # Calculate KPIs
    stats = data_loader.get_summary_stats(season, year)
    
    # Create donut chart
    from components.charts.donut_chart import DonutChart
    donut_fig = DonutChart.create_figure(
        stats["total_area"],
        stats["burned_area"],
        stats["difference"],
        Formatters.format_scope(season, year)
    )
    
    # Create trend chart
    trend_df = data_loader.get_trend_data(season)
    
    # Create trend figure
    bar = go.Bar(
        x=trend_df["Year"],
        y=trend_df["Area"],
        name="Area under Production",
        marker_color="#60A5FA",
        opacity=0.9,
    )
    
    line = go.Scatter(
        x=trend_df["Year"],
        y=trend_df["RollingAvgPct"],
        name="Rolling Avg. % Diff (3y)",
        mode="lines+markers",
        line=dict(width=3, color="#F472B6"),
        yaxis="y2",
    )
    
    trend_fig = go.Figure(data=[bar, line])
    trend_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0B1730",
        font_color="#E5EEFF",
        margin=dict(t=20, r=20, b=40, l=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="", gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(title="Area (Hac)", gridcolor="rgba(255,255,255,0.06)"),
        yaxis2=dict(title="% Diff", overlaying="y", side="right", gridcolor="rgba(255,255,255,0.0)"),
    )
    
    # Return all values
    return (
        Formatters.format_number(stats["total_area"]),
        Formatters.format_scope(season, year),
        Formatters.format_number(stats["burned_area"]),
        Formatters.format_scope(season, year),
        Formatters.format_number(stats["difference"]),
        Formatters.format_scope(season, year),
        Formatters.format_percentage(stats["pct_avg"]),
        "Average across selection",
        donut_fig,
        Formatters.get_donut_title(season, year),
        trend_fig,
        Formatters.get_trend_title(season),
    )

@app.callback(
    Output("year-comparison-dd", "options"),
    [Input("comparison-season-dd", "value")]
)
def update_comparison_year_options(season):
    """Update year options for comparison based on season selection."""
    years = data_loader.get_years()
    # Remove "All" option for comparison
    return [{"label": str(year), "value": str(year)} for year in years if year != "All"]

@app.callback(
    [
        Output("area-comparison-fig", "figure"),
        Output("burned-comparison-fig", "figure"),
        Output("trend-comparison-fig", "figure")
    ],
    [Input("comparison-season-dd", "value"), Input("year-comparison-dd", "value")]
)
def update_comparison_charts(season, selected_years):
    """Update comparison charts based on season and selected years."""
    try:
        if not selected_years:
            selected_years = []
        
        comparison_figures = year_comparison.create_comparison_figures(season, selected_years)
        
        return (
            comparison_figures['area_comparison'],
            comparison_figures['burned_comparison'],
            comparison_figures['trend_comparison']
        )
    except Exception as e:
        print(f"Error in comparison callback: {e}")
        # Return empty figures on error
        empty_fig = go.Figure()
        empty_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0B1730",
            font_color="#E5EEFF",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            annotations=[dict(
                text="Error loading comparison data",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="#94A3B8")
            )]
        )
        return empty_fig, empty_fig, empty_fig

@app.callback(
    [
        Output("forecast-fig", "figure"),
        Output("forecast-metrics", "children")
    ],
    [
        Input("forecast-generate-btn", "n_clicks"),
        Input("forecast-metric-dd", "value"),
        Input("forecast-periods-slider", "value"),
        Input("forecast-model-radio", "value"),
        Input("forecasting-season-dd", "value")
    ]
)
def generate_forecast(n_clicks, metric, periods, model_type, season):
    """Generate forecast based on user input."""
    if n_clicks > 0:
        historical_data = forecasting.prepare_forecast_data(season, metric)
        
        if model_type == 'exponential':
            forecast_data, metrics = forecasting.exponential_smoothing_forecast(historical_data, periods)
        else:
            forecast_data, metrics = forecasting.arima_forecast(historical_data, periods)
        
        forecast_fig = forecasting.create_forecast_figure(historical_data, forecast_data, metric, season)
        
        metrics_display = [
            html.H4("Model Performance Metrics", style={"color": "var(--accent-color)", "marginBottom": "1rem"}),
            html.Div(className="metric-item", children=[
                html.Span("Mean Absolute Error (MAE):", style={"fontWeight": "600"}),
                html.Span(f"{Formatters.format_number(metrics.get('mae', 0))} hectares", className="metric-value")
            ]),
            html.Div(className="metric-item", children=[
                html.Span("Root Mean Squared Error (RMSE):", style={"fontWeight": "600"}),
                html.Span(f"{Formatters.format_number(metrics.get('rmse', 0))} hectares", className="metric-value")
            ]),
            html.Div(className="metric-item", children=[
                html.Span("Model Type:", style={"fontWeight": "600"}),
                html.Span(metrics.get('model_type', 'Unknown'), className="metric-value")
            ]),
            html.Div(
                style={"marginTop": "1rem", "fontSize": "0.8rem", "color": "var(--text-muted)"},
                children=[
                    "MAE: Average error magnitude",
                    html.Br(),
                    "RMSE: Emphasizes larger errors"
                ]
            )
        ]
        
        return forecast_fig, metrics_display
    
    return go.Figure(), []

# Callbacks for Trend Analysis
@app.callback(
    Output("trend-analysis-fig", "figure"),
    [Input("trend-analysis-tab", "n_clicks"),
     Input("trend-metric-dd", "value"),
     Input("trend-chart-type-dd", "value"),
     Input("trend-analysis-season-dd", "value")]
)
def update_trend_analysis(n_clicks, metric, chart_type, season):
    """Update trend analysis figure based on selected parameters."""
    if n_clicks > 0:
        return trend_analysis.create_trend_figure(season, metric, chart_type)
    return go.Figure()

@app.callback(
    Output("trend-stats", "children"),
    [Input("trend-analysis-tab", "n_clicks"),
     Input("trend-metric-dd", "value"),
     Input("trend-analysis-season-dd", "value")]
)
def update_trend_statistics(n_clicks, metric, season):
    """Update trend statistics based on selected parameters."""
    if n_clicks > 0:
        return trend_analysis.get_trend_statistics(season, metric)
    return []

# Callbacks for Export & Reports
@app.callback(
    [Output("export-download-link", "children"),
     Output("export-status", "children"),
     Output("download-section", "style")],
    [Input("export-generate-btn", "n_clicks"),
     Input("export-format-dd", "value"),
     Input("export-scope-dd", "value"),
     Input("export-metrics-checklist", "value"),
     Input("export-reports-season-dd", "value"),
     Input("export-reports-year-dd", "value")]
)
def generate_export(n_clicks, format_type, scope, metrics, season, year):
    """Generate export based on selected parameters."""
    print(f"Export callback triggered with n_clicks: {n_clicks}")
    print(f"Parameters - format: {format_type}, scope: {scope}, metrics: {metrics}, season: {season}, year: {year}")
    
    if n_clicks and n_clicks > 0:
        try:
            print("Processing export request...")
            if scope == "current":
                df = data_loader.filter_data(season, year)
            elif scope == "all":
                df = data_loader.df
            else:
                # Handle custom range logic if needed
                df = data_loader.filter_data(season, year)  # Placeholder for custom logic
            
            print(f"DataFrame shape: {df.shape}")
            
            if df.empty:
                print("No data available for export")
                return "", "No data available for export", {"display": "none"}
            
            if format_type == "csv":
                filename = export_reports.get_export_filename(season, year, format_type)
                # Create a download link using base64 encoding
                csv_string = df.to_csv(index=False)
                b64 = base64.b64encode(csv_string.encode()).decode()
                href = f"data:text/csv;base64,{b64}"
                download_link = html.A(
                    f"Download {filename}",
                    href=href,
                    download=filename,
                    className="btn-primary"
                )
                print("CSV export ready")
                return download_link, "CSV export ready for download", {"display": "block"}
            elif format_type == "pdf":
                # Generate actual PDF report
                filename = export_reports.get_export_filename(season, year, format_type)
                export_data = export_reports.generate_pdf_report(df, season, year)
                if export_data["error"]:
                    print(f"PDF generation error: {export_data['error']}")
                    return "", f"Error: {export_data['error']}", {"display": "none"}
                
                # Create download link for PDF
                download_link = html.A(
                    f"Download {filename}",
                    href=export_data["content"],
                    download=filename,
                    className="btn-primary"
                )
                print("PDF export ready")
                return download_link, "PDF report ready for download", {"display": "block"}
        
        except Exception as e:
            print(f"Error generating export: {str(e)}")
            return "", f"Error generating export: {str(e)}", {"display": "none"}
    
    print("No export generated (n_clicks <= 0)")
    return "", "", {"display": "none"}

if __name__ == "__main__":
    app.run(debug=True, port=8050)
