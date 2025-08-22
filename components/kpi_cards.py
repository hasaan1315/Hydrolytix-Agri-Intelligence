"""
KPI cards component for displaying key metrics.
"""

import dash
from dash import html
from utils.formatters import Formatters
from config import colors

class KPICards:
    """KPI cards component for displaying key metrics."""
    
    def create_kpi_row(self) -> html.Div:
        """Create the KPI cards row."""
        
        return html.Div(
            className="kpi-row",
            children=[
                self._create_kpi_card(
                    title="Total Area (Hac)",
                    value_id="kpi-area",
                    subtitle_id="kpi-area-sub"
                ),
                self._create_kpi_card(
                    title="Burned Area (Hac)",
                    value_id="kpi-burned",
                    subtitle_id="kpi-burned-sub"
                ),
                self._create_kpi_card(
                    title="Difference (Hac)",
                    value_id="kpi-diff",
                    subtitle_id="kpi-diff-sub"
                ),
                self._create_kpi_card(
                    title="% Difference (avg.)",
                    value_id="kpi-pct",
                    subtitle_id="kpi-pct-sub",
                    accent=True
                ),
            ],
        )
    
    def _create_kpi_card(self, title: str, value_id: str, subtitle_id: str, accent: bool = False) -> html.Div:
        """Create individual KPI card."""
        
        value_class = "kpi-value accent" if accent else "kpi-value"
        
        return html.Div(
            className="kpi",
            children=[
                html.Div(title, className="kpi-title"),
                html.Div(id=value_id, className=value_class),
                html.Div(id=subtitle_id, className="kpi-sub"),
            ],
        )
