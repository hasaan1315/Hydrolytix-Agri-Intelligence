"""
Navigation bar component for the dashboard.
"""

import dash
from dash import html
from datetime import datetime
from config import settings, colors

def create_navbar() -> html.Div:
    """Create the navigation bar component."""
    
    return html.Div(
        className="navbar",
        children=[
            # Brand section
            html.Div(className="brand", children=[
                html.Div(className="logo-dot"),
                html.Span("Hydrolytix", className="brand-name"),
                html.Span("Agri Intelligence", className="brand-tag")
            ]),
            
            # Right section with last updated
            html.Div(
                className="navbar-right",
                children=[
                    html.Div(
                        className="updated",
                        children=f"Last Updated: {datetime.utcnow().strftime('%b %d, %Y %H:%M (UTC)')}",
                    ),
                ]
            ),
        ],
    )
