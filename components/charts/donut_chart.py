"""
Donut chart component for composition visualization.
"""

import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
from utils.formatters import Formatters
from config import colors

class DonutChart:
    """Donut chart component for composition visualization."""
    
    def create_donut_card(self) -> html.Div:
        """Create the donut chart card."""
        
        return html.Div(
            className="card donut-card",
            children=[
                html.Div(id="donut-title", className="card-title"),
                dcc.Graph(
                    id="donut-fig", 
                    config={"displayModeBar": False},
                    style={"height": "320px", "width": "100%"}
                ),
            ],
        )
    
    @staticmethod
    def create_figure(area: float, burned: float, difference: float, scope: str) -> go.Figure:
        """Create the donut chart figure."""
        
        # Prepare data
        labels = ["Area under Production", "Burned Area", "Difference"]
        values = [
            max(area, 0),
            max(burned, 0),
            max(difference, 0),
        ]
        
        # Create figure
        fig = px.pie(
            names=labels,
            values=values,
            hole=0.55,
            color=labels,
            color_discrete_map={
                "Area under Production": colors.CHART_COLORS["production"],
                "Burned Area": colors.CHART_COLORS["burned"],
                "Difference": colors.CHART_COLORS["difference"],
            },
        )
        
        # Update layout
        fig.update_traces(textinfo="percent+label")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color=colors.TEXT["primary"],
            margin=dict(t=10, r=10, b=10, l=10),
            showlegend=False,
        )
        
        return fig
