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
from utils.data_loader import DataLoader

class DashboardLayout:
    """Main dashboard layout component."""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
        self.overview_filter_controls = FilterControls(data_loader)
        self.comparison_filter_controls = FilterControls(data_loader)
        self.forecasting_filter_controls = FilterControls(data_loader)
        self.kpi_cards = KPICards()
        self.donut_chart = DonutChart()
        self.year_comparison = YearComparison(data_loader)
        self.forecasting = Forecasting(data_loader)
    
    def create_layout(self) -> html.Div:
        """Create the main dashboard layout."""
        
        return html.Div(
            id="app-container",
            className="app",
            children=[
                create_navbar(),
                
                dcc.Tabs(
                    id="main-tabs",
                    value="overview",
                    children=[
                        dcc.Tab(
                            label="Overview",
                            value="overview",
                            children=self._create_overview_layout()
                        ),
                        dcc.Tab(
                            label="Year Comparison", 
                            value="comparison",
                            children=self._create_comparison_layout()
                        ),
                        dcc.Tab(
                            label="Forecasting",
                            value="forecasting",
                            children=self._create_forecasting_layout()
                        )
                    ]
                )
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
