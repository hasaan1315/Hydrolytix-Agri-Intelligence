"""
Main layout component for the dashboard.
"""

import dash
from dash import html
from components.navbar import create_navbar
from components.filters import FilterControls
from components.kpi_cards import KPICards
from components.charts.donut_chart import DonutChart
from utils.data_loader import DataLoader

class DashboardLayout:
    """Main dashboard layout component."""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
        self.filter_controls = FilterControls(data_loader)
        self.kpi_cards = KPICards()
        self.donut_chart = DonutChart()
    
    def create_layout(self) -> html.Div:
        """Create the main dashboard layout."""
        
        return html.Div(
            id="app-container",
            className="app",
            children=[
                create_navbar(),
                
                html.Div(
                    className="grid",
                    children=[
                        # Filter Card
                        self.filter_controls.create_filter_card(),
                        
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
                ),
            ],
        )
