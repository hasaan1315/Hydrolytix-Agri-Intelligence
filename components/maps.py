"""
Interactive Maps Component for geographical data visualization
"""

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from utils.data_loader import DataLoader

class InteractiveMaps:
    """Interactive maps for geographical data visualization."""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def create_choropleth_map(self, season=None, year=None):
        """Create interactive choropleth map for agricultural data."""
        
        # Get filtered data
        df = self.data_loader.filter_data(season, year)
        
        # Group by district for geographical visualization
        district_data = df.groupby('District').agg({
            'Area': 'sum',
            'Production': 'sum',
            'Yield': 'mean',
            'Burned_Area': 'sum'
        }).reset_index()
        
        # Create choropleth map
        fig = px.choropleth_mapbox(
            district_data,
            locations='District',
            color='Production',
            color_continuous_scale='Viridis',
            mapbox_style='carto-positron',
            zoom=6,
            center={'lat': 31.1471, 'lon': 75.3412},
            opacity=0.7,
            labels={'Production': 'Production (Tons)'},
            title='Agricultural Production by District'
        )
        
        fig.update_layout(
            margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E5EEFF'
        )
        
        return fig
    
    def create_scatter_map(self, season=None, year=None):
        """Create scatter map for detailed location data."""
        
        df = self.data_loader.filter_data(season, year)
        
        # Sample data for scatter plot (if coordinates available)
        if 'Latitude' in df.columns and 'Longitude' in df.columns:
            fig = px.scatter_mapbox(
                df,
                lat='Latitude',
                lon='Longitude',
                color='Yield',
                size='Area',
                color_continuous_scale='Bluered',
                size_max=15,
                zoom=6,
                mapbox_style='carto-positron',
                title='Farm Locations & Performance'
            )
            
            fig.update_layout(
                margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#E5EEFF'
            )
            
            return fig
        
        return None
    
    def create_map_card(self):
        """Create map visualization card."""
        
        return html.Div(
            className="card map-card",
            children=[
                html.H3("Geographical Analysis", className="card-title"),
                dcc.Tabs(
                    id="map-tabs",
                    value="choropleth",
                    children=[
                        dcc.Tab(
                            label="District Overview",
                            value="choropleth",
                            children=[
                                dcc.Graph(
                                    id="choropleth-map",
                                    config={'displayModeBar': False}
                                )
                            ]
                        ),
                        dcc.Tab(
                            label="Farm Locations",
                            value="scatter",
                            children=[
                                dcc.Graph(
                                    id="scatter-map",
                                    config={'displayModeBar': False}
                                )
                            ]
                        )
                    ]
                )
            ]
        )
