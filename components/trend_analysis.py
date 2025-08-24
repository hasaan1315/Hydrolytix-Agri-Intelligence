"""
Trend Analysis component for advanced agricultural data visualization.
"""

import dash
from dash import html, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Any
from utils.data_loader import DataLoader

class TrendAnalysis:
    """Advanced trend analysis and visualization component."""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
    
    def create_trend_analysis_card(self) -> html.Div:
        """Create the trend analysis card layout."""
        return html.Div(
            className="card trend-analysis-card",
            children=[
                html.H3("Advanced Trend Analysis", className="card-title"),
                html.Div(
                    className="trend-controls",
                    children=[
                        html.Label("Select Metric:"),
                        dcc.Dropdown(
                            id="trend-metric-dd",
                            options=[
                                {"label": "Area under Production", "value": "area"},
                                {"label": "Burned Area", "value": "burned"},
                                {"label": "Difference", "value": "difference"},
                                {"label": "% Difference", "value": "pct_diff"}
                            ],
                            value="area",
                            className="dropdown"
                        ),
                        html.Label("Chart Type:"),
                        dcc.Dropdown(
                            id="trend-chart-type-dd",
                            options=[
                                {"label": "Line Chart", "value": "line"},
                                {"label": "Area Chart", "value": "area"},
                                {"label": "Scatter Plot", "value": "scatter"}
                            ],
                            value="line",
                            className="dropdown"
                        )
                    ]
                ),
                dcc.Graph(
                    id="trend-analysis-fig",
                    style={"height": "400px", "width": "100%"}
                ),
                html.Div(
                    className="statistics-summary",
                    children=[
                        html.H4("Statistical Summary", className="summary-title"),
                        html.Div(id="trend-stats", className="stats-grid")
                    ]
                )
            ],
        )
    
    def create_trend_figure(self, season: str, metric: str, chart_type: str) -> go.Figure:
        """Create trend analysis figure based on selected parameters."""
        df = self.data_loader.filter_data(season, "All")
        
        if df.empty:
            return self._create_empty_figure("No data available for selected season")
        
        # Group by year and season for comparison
        trend_data = df.groupby(["Year", "Season"]).agg({
            "Area under Production (Hac)": "sum",
            "Burned Area (Hac)": "sum", 
            "Difference (Hac)": "sum",
            "% Difference Numeric": "mean"
        }).reset_index()
        
        fig = make_subplots(
            rows=1, cols=1,
            subplot_titles=[f"Trend Analysis - {season if season != 'All' else 'All Seasons'}"]
        )
        
        metrics_map = {
            "area": "Area under Production (Hac)",
            "burned": "Burned Area (Hac)",
            "difference": "Difference (Hac)",
            "pct_diff": "% Difference Numeric"
        }
        
        selected_metric = metrics_map[metric]
        
        if season == "All":
            # Show both seasons
            for season_type in ["Rabi", "Kharif"]:
                season_df = trend_data[trend_data["Season"] == season_type]
                self._add_trace_to_fig(fig, season_df, season_type, selected_metric, chart_type)
        else:
            # Show selected season only
            self._add_trace_to_fig(fig, trend_data, season, selected_metric, chart_type)
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0B1730",
            font_color="#E5EEFF",
            margin=dict(t=40, r=20, b=40, l=60),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(title="Year", gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(title=selected_metric, gridcolor="rgba(255,255,255,0.06)"),
        )
        
        return fig
    
    def _add_trace_to_fig(self, fig: go.Figure, data: pd.DataFrame, 
                         name: str, metric: str, chart_type: str) -> None:
        """Add trace to figure based on chart type."""
        if chart_type == "line":
            fig.add_trace(go.Scatter(
                x=data["Year"],
                y=data[metric],
                name=name,
                mode="lines+markers",
                line=dict(width=3),
                marker=dict(size=8)
            ))
        elif chart_type == "area":
            fig.add_trace(go.Scatter(
                x=data["Year"],
                y=data[metric],
                name=name,
                mode="lines",
                fill="tozeroy",
                line=dict(width=2)
            ))
        elif chart_type == "scatter":
            fig.add_trace(go.Scatter(
                x=data["Year"],
                y=data[metric],
                name=name,
                mode="markers",
                marker=dict(size=10, opacity=0.7)
            ))
    
    def get_trend_statistics(self, season: str, metric: str) -> List[html.Div]:
        """Get statistical summary for the selected trend data."""
        df = self.data_loader.filter_data(season, "All")
        
        if df.empty:
            return [html.Div("No data available", className="stat-item")]
        
        metrics_map = {
            "area": "Area under Production (Hac)",
            "burned": "Burned Area (Hac)",
            "difference": "Difference (Hac)",
            "pct_diff": "% Difference Numeric"
        }
        
        selected_metric = metrics_map[metric]
        values = df[selected_metric]
        
        stats = {
            "Mean": values.mean(),
            "Median": values.median(),
            "Std Dev": values.std(),
            "Min": values.min(),
            "Max": values.max(),
            "Total": values.sum() if metric != "pct_diff" else "N/A"
        }
        
        return [
            html.Div([
                html.Span(f"{stat_name}:", className="stat-label"),
                html.Span(f"{stat_value:.2f}" if isinstance(stat_value, (int, float)) else stat_value, 
                         className="stat-value")
            ], className="stat-item")
            for stat_name, stat_value in stats.items()
        ]
    
    def _create_empty_figure(self, message: str) -> go.Figure:
        """Create empty figure with message."""
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0B1730",
            font_color="#E5EEFF",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            annotations=[dict(
                text=message,
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="#94A3B8")
            )]
        )
        return fig
