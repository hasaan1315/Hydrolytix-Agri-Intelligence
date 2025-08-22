"""
Hydrolytix Agri Dashboard - Clean, Modular Architecture
Main application entry point with clean styling and modular components.
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from datetime import datetime
 
# Import modular components
from utils.data_loader import DataLoader
from utils.formatters import Formatters
from components.layout import DashboardLayout
from components.comparison import YearComparison

# Initialize data loader
data_loader = DataLoader("agri_analysis_punjab_clean.csv")

# Initialize comparison component
year_comparison = YearComparison(data_loader)

# Create the app
app = dash.Dash(__name__, 
                external_stylesheets=["https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"])
app.title = "Hydrolytix • Agri Intelligence"

# Create layout
dashboard_layout = DashboardLayout(data_loader)
app.layout = dashboard_layout.create_layout()

# Callbacks
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
    [Input("season-dd", "value"), Input("year-dd", "value")],
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
    [Input("season-dd", "value")]
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
    [Input("season-dd", "value"), Input("year-comparison-dd", "value")]
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

if __name__ == "__main__":
    app.run(debug=True, port=8050)
