"""
Multi-Year Comparison Component
Enables side-by-side comparison of agricultural metrics across different years
"""

import dash
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict, Any
from utils.data_loader import DataLoader
from utils.formatters import Formatters

class YearComparison:
    """Handles multi-year comparison visualizations."""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
    
    def create_comparison_figures(self, season: str, years: List[str]) -> Dict[str, go.Figure]:
        """Create comparison figures for multiple years."""
        
        # Handle edge cases: no years selected, "All" selected, or less than 2 years
        if not years or years == ["All"] or len(years) < 2:
            return self._create_empty_comparison()
        
        # Get data for selected years
        comparison_data = {}
        for year in years:
            if year != "All":
                try:
                    df = self.data_loader.filter_data(season, year)
                    stats = self.data_loader.get_summary_stats(season, year)
                    comparison_data[year] = {
                        'stats': stats,
                        'trend_data': self.data_loader.get_trend_data(season)
                    }
                except Exception as e:
                    print(f"Error processing year {year}: {e}")
                    continue
        
        # If we don't have enough valid data, return empty comparison
        if len(comparison_data) < 2:
            return self._create_empty_comparison()
        
        # Create comparison figures
        return {
            'area_comparison': self._create_area_comparison_chart(comparison_data, season),
            'burned_comparison': self._create_burned_comparison_chart(comparison_data, season),
            'trend_comparison': self._create_trend_comparison_chart(comparison_data, season)
        }
    
    def _create_area_comparison_chart(self, comparison_data: Dict, season: str) -> go.Figure:
        """Create area under production comparison chart."""
        years = list(comparison_data.keys())
        areas = [comparison_data[year]['stats']['total_area'] for year in years]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=years,
            y=areas,
            name="Area under Production",
            marker_color='#60A5FA',
            text=[Formatters.format_number(area) for area in areas],
            textposition='auto',
        ))
        
        fig.update_layout(
            title=f"Area Comparison - {season if season != 'All' else 'All Seasons'}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0B1730",
            font_color="#E5EEFF",
            margin=dict(t=50, r=20, b=40, l=40),
            xaxis=dict(title="Year"),
            yaxis=dict(title="Area (Hac)"),
            showlegend=False
        )
        
        return fig
    
    def _create_burned_comparison_chart(self, comparison_data: Dict, season: str) -> go.Figure:
        """Create burned area comparison chart."""
        years = list(comparison_data.keys())
        burned_areas = [comparison_data[year]['stats']['burned_area'] for year in years]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=years,
            y=burned_areas,
            name="Burned Area",
            marker_color='#F472B6',
            text=[Formatters.format_number(area) for area in burned_areas],
            textposition='auto',
        ))
        
        fig.update_layout(
            title=f"Burned Area Comparison - {season if season != 'All' else 'All Seasons'}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0B1730",
            font_color="#E5EEFF",
            margin=dict(t=50, r=20, b=40, l=40),
            xaxis=dict(title="Year"),
            yaxis=dict(title="Burned Area (Hac)"),
            showlegend=False
        )
        
        return fig
    
    def _create_trend_comparison_chart(self, comparison_data: Dict, season: str) -> go.Figure:
        """Create trend comparison chart with multiple lines showing individual year data."""
        fig = go.Figure()
        
        colors = ['#60A5FA', '#F472B6', '#10B981', '#F59E0B', '#818CF8']
        
        # Get all unique years from the data to create a proper timeline
        all_years = []
        for year_data in comparison_data.values():
            if 'trend_data' in year_data:
                all_years.extend(year_data['trend_data']['Year'].tolist())
        
        if not all_years:
            return self._create_empty_trend_chart()
        
        min_year = min(all_years)
        max_year = max(all_years)
        
        # Create data points for each selected year
        for i, (selected_year, data) in enumerate(comparison_data.items()):
            if 'trend_data' in data:
                trend_df = data['trend_data']
                # Filter to only show data for the specific selected year
                year_data = trend_df[trend_df['Year'] == int(selected_year)]
                if not year_data.empty:
                    fig.add_trace(go.Scatter(
                        x=[year_data['Year'].iloc[0]],
                        y=[year_data['Area'].iloc[0]],
                        name=f"{selected_year} Area",
                        line=dict(color=colors[i % len(colors)], width=3),
                        mode='markers+text',
                        text=[f"{selected_year}"],
                        textposition="top center",
                        marker=dict(size=12),
                        textfont=dict(size=10)
                    ))
        
        # Add a smooth trend line showing the overall pattern (solid line)
        overall_trend = self.data_loader.get_trend_data(season)
        fig.add_trace(go.Scatter(
            x=overall_trend['Year'],
            y=overall_trend['Area'],
            name="Overall Trend",
            line=dict(color='rgba(255, 255, 255, 0.5)', width=2),
            mode='lines',
            opacity=0.7
        ))
        
        fig.update_layout(
            title=f"Multi-Year Comparison - {season if season != 'All' else 'All Seasons'}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0B1730",
            font_color="#E5EEFF",
            margin=dict(t=50, r=20, b=40, l=40),
            xaxis=dict(
                title="Year",
                range=[min_year - 0.5, max_year + 0.5],
                tickmode='linear',
                dtick=1
            ),
            yaxis=dict(title="Area (Hac)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            showlegend=True
        )
        
        return fig
    
    def _create_empty_trend_chart(self) -> go.Figure:
        """Create empty trend chart placeholder."""
        empty_fig = go.Figure()
        empty_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0B1730",
            font_color="#E5EEFF",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            annotations=[dict(
                text="Select multiple years for trend comparison",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="#94A3B8")
            )]
        )
        return empty_fig
    
    def _create_empty_comparison(self) -> Dict[str, go.Figure]:
        """Create empty comparison figures placeholder."""
        empty_fig = go.Figure()
        empty_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0B1730",
            font_color="#E5EEFF",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            annotations=[dict(
                text="Select multiple years for comparison",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="#94A3B8")
            )]
        )
        
        return {
            'area_comparison': empty_fig,
            'burned_comparison': empty_fig,
            'trend_comparison': empty_fig
        }
    
    def create_comparison_card(self):
        """Create the comparison visualization card."""
        return html.Div(
            className="card comparison-card",
            children=[
                html.H3("Multi-Year Comparison", className="card-title"),
                html.Div(
                    className="comparison-controls",
                    children=[
                        html.Label("Select Years to Compare:", className="filter-label"),
                        dcc.Dropdown(
                            id="year-comparison-dd",
                            multi=True,
                            placeholder="Select years...",
                            className="dropdown"
                        )
                    ]
                ),
                html.Div(
                    className="comparison-charts",
                    children=[
                        dcc.Graph(
                            id="area-comparison-fig",
                            config={'displayModeBar': True},
                            style={"height": "300px"}
                        ),
                        dcc.Graph(
                            id="burned-comparison-fig", 
                            config={'displayModeBar': True},
                            style={"height": "300px"}
                        ),
                        dcc.Graph(
                            id="trend-comparison-fig",
                            config={'displayModeBar': True},
                            style={"height": "350px"}
                        )
                    ]
                )
            ]
        )
