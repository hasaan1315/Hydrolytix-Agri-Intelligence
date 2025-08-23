"""
Filter controls component for the dashboard.
"""

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from utils.data_loader import DataLoader
from config import settings, colors

class FilterControls:
    """Filter controls component."""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
    
    def create_filter_card(self, id_prefix: str) -> html.Div:
        """Create the filter card component."""
        
        seasons = self.data_loader.get_seasons()
        years = self.data_loader.get_years()
        
        return html.Div(
            className="card filter-card",
            children=[
                html.H3("Filters"),
                
                html.Label("Season", className="filter-label"),
                dcc.Dropdown(
                    id=f"{id_prefix}-season-dd",
                    options=[{"label": s, "value": s} for s in seasons],
                    value="All",
                    className="dropdown",
                    clearable=False,
                ),
                
                html.Label("Year", className="filter-label"),
                dcc.Dropdown(
                    id=f"{id_prefix}-year-dd",
                    options=[{"label": str(y), "value": y} for y in years],
                    value="All",
                    className="dropdown",
                    clearable=False,
                ),
                
                html.Div(
                    className="note",
                    children="Tip: Choose Season=All to compare Rabi vs Kharif."
                ),
            ],
        )
