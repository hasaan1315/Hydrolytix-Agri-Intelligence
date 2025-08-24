"""
Main layout component for the dashboard.
"""

import dash
from dash import html, dcc
from components.navbar import create_navbar
from components.filters import FilterControls
from components.kpi_cards import KPICards
from components.charts.donut_chart import DonutChart
from components.comparison import YearComparison
from components.forecasting import Forecasting
from components.trend_analysis import TrendAnalysis
from components.export_reports import ExportReports
from utils.data_loader import DataLoader

class DashboardLayout:
    """Main dashboard layout component."""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
        self.overview_filter_controls = FilterControls(data_loader)
        self.comparison_filter_controls = FilterControls(data_loader)
        self.forecasting_filter_controls = FilterControls(data_loader)
        self.trend_analysis_filter_controls = FilterControls(data_loader)
        self.export_filter_controls = FilterControls(data_loader)
        self.kpi_cards = KPICards()
        self.donut_chart = DonutChart()
        self.year_comparison = YearComparison(data_loader)
        self.forecasting = Forecasting(data_loader)
        self.trend_analysis = TrendAnalysis(data_loader)
        self.export_reports = ExportReports(data_loader)
    
    def create_layout(self) -> html.Div:
        """Create the main dashboard layout."""
        
        return html.Div(
            id="app-container",
            className="app",
            children=[
                create_navbar(),
                
                # Custom tabs implementation for better styling control
                html.Div([
                    html.Div([
                        html.Button(
                            "Overview",
                            id="overview-tab",
                            className="custom-tab active",
                            n_clicks=0
                        ),
                        html.Button(
                            "Year Comparison",
                            id="comparison-tab",
                            className="custom-tab",
                            n_clicks=0
                        ),
                        html.Button(
                            "Forecasting",
                            id="forecasting-tab",
                            className="custom-tab",
                            n_clicks=0
                        ),
                        html.Button(
                            "Trend Analysis",
                            id="trend-analysis-tab",
                            className="custom-tab",
                            n_clicks=0
                        ),
                        html.Button(
                            "Export & Reports",
                            id="export-reports-tab",
                            className="custom-tab",
                            n_clicks=0
                        )
                    ], className="custom-tabs-container"),
                    
                    html.Div(self._create_overview_layout(), id="tab-content")
                ])
            ],
        )
    
    def _create_overview_layout(self) -> html.Div:
        """Create the overview tab layout."""
        return html.Div(
            className="grid",
            children=[
                # Filter Card
                self.overview_filter_controls.create_filter_card("overview"),
                
                # KPI Cards Row
                self.kpi_cards.create_kpi_row(),
                
                # Donut Chart Card
                self.donut_chart.create_donut_card(),
                
                # Trend Chart Card
                html.Div(
                    className="card trend-card",
                    children=[
                        html.Div(id="trend-title", className="card-title"),
                        dash.dcc.Graph(
                            id="trend-fig",
                            style={"height": "320px", "width": "100%"}
                        ),
                    ],
                ),
            ],
        )
    
    def _create_comparison_layout(self) -> html.Div:
        """Create the comparison tab layout."""
        return html.Div(
            className="grid-comparison",
            children=[
                # Filter Card
                self.comparison_filter_controls.create_filter_card("comparison"),
                
                # Comparison Card
                self.year_comparison.create_comparison_card()
            ],
        )
    
    def _create_forecasting_layout(self) -> html.Div:
        """Create the forecasting tab layout."""
        return html.Div(
            className="grid-comparison",
            children=[
                # Filter Card
                self.forecasting_filter_controls.create_filter_card("forecasting"),
                
                # Forecasting Card
                self.forecasting.create_forecast_card()
            ],
        )
    
    def _create_trend_analysis_layout(self) -> html.Div:
        """Create the trend analysis tab layout."""
        return html.Div(
            className="grid-comparison",
            children=[
                # Filter Card
                self.trend_analysis_filter_controls.create_filter_card("trend-analysis"),
                
                # Trend Analysis Card
                self.trend_analysis.create_trend_analysis_card()
            ],
        )
    
    def _create_export_reports_layout(self) -> html.Div:
        """Create the export and reports tab layout."""
        return html.Div(
            className="grid-comparison",
            children=[
                # Filter Card
                self.export_filter_controls.create_filter_card("export-reports"),
                
                # Export & Reports Card
                self.export_reports.create_export_card()
            ],
        )
