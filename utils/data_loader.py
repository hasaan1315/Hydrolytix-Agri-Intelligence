"""
Data loading and processing utilities.
"""

import pandas as pd
from typing import Tuple, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Handles data loading and preprocessing."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self._load_data()
    
    def _load_data(self) -> None:
        """Load and preprocess the data."""
        try:
            self.df = pd.read_csv(self.file_path)
            self._clean_data()
            logger.info(f"Successfully loaded data from {self.file_path}")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _clean_data(self) -> None:
        """Clean and normalize the data."""
        # Normalize column names
        self.df.columns = [c.strip() for c in self.df.columns]
        
        # Ensure proper data types
        self.df["Year"] = self.df["Year"].astype(int)
        
        # Add numeric percentage difference if not exists
        if "% Difference Numeric" not in self.df.columns:
            self.df["% Difference Numeric"] = (
                self.df["% Difference"]
                .astype(str)
                .str.replace("%", "", regex=False)
                .astype(float)
            )
    
    def get_seasons(self) -> List[str]:
        """Get unique seasons."""
        return ["All"] + sorted(self.df["Season"].unique().tolist())
    
    def get_years(self) -> List[str]:
        """Get unique years."""
        return ["All"] + sorted(self.df["Year"].unique().tolist())
    
    def filter_data(self, season: str, year: str) -> pd.DataFrame:
        """Filter data based on season and year."""
        filtered_df = self.df.copy()
        
        if season != "All":
            filtered_df = filtered_df[filtered_df["Season"] == season]
        
        if year != "All":
            filtered_df = filtered_df[filtered_df["Year"] == int(year)]
        
        return filtered_df
    
    def get_summary_stats(self, season: str, year: str) -> Dict[str, float]:
        """Get summary statistics for KPIs."""
        df = self.filter_data(season, year)
        
        return {
            "total_area": df["Area under Production (Hac)"].sum(),
            "burned_area": df["Burned Area (Hac)"].sum(),
            "difference": df["Difference (Hac)"].sum(),
            "pct_avg": df["% Difference Numeric"].mean()
        }
    
    def get_trend_data(self, season: str) -> pd.DataFrame:
        """Get trend data for charts."""
        df = self.filter_data(season, "All")
        df = df.sort_values("Year")
        
        # Aggregate by year
        trend_agg = (
            df.groupby("Year", as_index=False)
            .agg({
                "Area under Production (Hac)": "sum",
                "% Difference Numeric": "mean",
            })
            .rename(columns={
                "Area under Production (Hac)": "Area",
                "% Difference Numeric": "Pct"
            })
        )
        
        # Add rolling average
        trend_agg["RollingAvgPct"] = trend_agg["Pct"].rolling(3, min_periods=1).mean()
        
        return trend_agg
