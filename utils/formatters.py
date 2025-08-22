"""
Data formatting and display utilities.
"""

from typing import Union, Optional
import pandas as pd

class Formatters:
    """Utility class for formatting data for display."""
    
    @staticmethod
    def format_number(value: Union[int, float, None], 
                     decimals: int = 0, 
                     suffix: str = "") -> str:
        """Format numbers with thousand separators."""
        if value is None or pd.isna(value):
            return "—"
        
        try:
            formatted = f"{float(value):,.{decimals}f}"
            # Remove .0 for integers
            if decimals == 0:
                formatted = formatted.rstrip('0').rstrip('.')
            return formatted + suffix
        except (ValueError, TypeError):
            return "—"
    
    @staticmethod
    def format_percentage(value: Union[float, None], 
                         decimals: int = 1) -> str:
        """Format percentage values."""
        if value is None or pd.isna(value):
            return "—%"
        
        try:
            return f"{float(value):.{decimals}f}%"
        except (ValueError, TypeError):
            return "—%"
    
    @staticmethod
    def format_scope(season: str, year: str) -> str:
        """Format the scope text for titles and subtitles."""
        if season == "All" and year == "All":
            return "All Data"
        elif season == "All":
            return f"Year {year}"
        elif year == "All":
            return season
        else:
            return f"{season}, {year}"
    
    @staticmethod
    def format_kpi_subtitle(season: str, year: str) -> str:
        """Format subtitle for KPI cards."""
        scope = Formatters.format_scope(season, year)
        if scope == "All Data":
            return "All Data"
        return scope
    
    @staticmethod
    def get_trend_title(season: str) -> str:
        """Generate trend chart title."""
        season_text = season if season != "All" else "All Seasons"
        return f"Yearly Area & 3-Year Rolling % Difference • {season_text}"
    
    @staticmethod
    def get_donut_title(season: str, year: str) -> str:
        """Generate donut chart title."""
        scope = Formatters.format_scope(season, year)
        return f"Composition • {scope}"
