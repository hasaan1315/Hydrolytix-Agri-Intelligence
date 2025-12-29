"""
Export and Reports component for data export functionality.
"""

import dash
from dash import html, dcc
import pandas as pd
import base64
from io import BytesIO
from typing import Dict, List, Any
from utils.data_loader import DataLoader
from utils.formatters import Formatters
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ExportReports:
    """Data export and report generation component."""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
    
    def create_export_card(self) -> html.Div:
        """Create the export and reports card layout."""
        seasons = self.data_loader.get_seasons()
        years = self.data_loader.get_years()
        
        return html.Div(
            className="card export-card",
            children=[
                html.H3("Export & Reports", className="card-title"),
                
                # Export Controls
                html.Div(
                    className="export-controls",
                    children=[
                        html.Div([
                            html.Label("Season:"),
                            dcc.Dropdown(
                                id="export-reports-season-dd",
                                options=[{"label": s, "value": s} for s in seasons],
                                value="All",
                                className="dropdown"
                            )
                        ]),
                        
                        html.Div([
                            html.Label("Year:"),
                            dcc.Dropdown(
                                id="export-reports-year-dd",
                                options=[{"label": str(y), "value": y} for y in years],
                                value="All",
                                className="dropdown"
                            )
                        ]),
                        
                        html.Div([
                            html.Label("Export Format:"),
                            dcc.Dropdown(
                                id="export-format-dd",
                                options=[
                                    {"label": "CSV", "value": "csv"},
                                    {"label": "PDF Report", "value": "pdf"}
                                ],
                                value="csv",
                                className="dropdown"
                            )
                        ]),
                        
                        html.Div([
                            html.Label("Data Scope:"),
                            dcc.Dropdown(
                                id="export-scope-dd",
                                options=[
                                    {"label": "Current View", "value": "current"},
                                    {"label": "All Data", "value": "all"},
                                    {"label": "Custom Range", "value": "custom"}
                                ],
                                value="current",
                                className="dropdown"
                            )
                        ]),
                        
                        html.Div([
                            html.Label("Include Metrics:"),
                            dcc.Checklist(
                                id="export-metrics-checklist",
                                options=[
                                    {"label": "Area under Production", "value": "area"},
                                    {"label": "Burned Area", "value": "burned"},
                                    {"label": "Difference", "value": "difference"},
                                    {"label": "% Difference", "value": "pct_diff"}
                                ],
                                value=["area", "burned", "difference", "pct_diff"],
                                className="checklist"
                            )
                        ]),
                        
                        html.Button(
                            "Generate Export",
                            id="export-generate-btn",
                            className="btn-primary",
                            n_clicks=0
                        )
                    ]
                ),
                
                # Download Section
                html.Div(
                    id="download-section",
                    className="download-section",
                    children=[
                        html.H4("Download Ready", className="download-title"),
                        html.Div(id="export-download-link", className="download-link"),
                        html.Div(id="export-status", className="status-message")
                    ],
                    style={"display": "none"}
                ),
                
                # Report Preview
                html.Div(
                    className="report-preview",
                    children=[
                        html.H4("Report Preview", className="preview-title"),
                        html.Div(id="report-preview-content", className="preview-content")
                    ]
                )
            ],
        )
    
    def prepare_export_data(self, season: str, year: str, metrics: List[str]) -> pd.DataFrame:
        """Prepare data for export based on selected parameters."""
        df = self.data_loader.filter_data(season, year)
        
        if df.empty:
            return pd.DataFrame()
        
        # Select only requested columns
        column_map = {
            "area": "Area under Production (Hac)",
            "burned": "Burned Area (Hac)",
            "difference": "Difference (Hac)",
            "pct_diff": "% Difference Numeric"
        }
        
        base_columns = ["Year", "Season"]
        selected_columns = base_columns + [column_map[metric] for metric in metrics if metric in column_map]
        
        return df[selected_columns].copy()
    
    def generate_csv_export(self, df: pd.DataFrame, filename: str) -> Dict[str, str]:
        """Generate CSV export and return download link."""
        if df.empty:
            return {"content": "", "filename": "", "error": "No data to export"}
        
        csv_string = df.to_csv(index=False)
        b64 = base64.b64encode(csv_string.encode()).decode()
        
        return {
            "content": f"data:text/csv;base64,{b64}",
            "filename": f"{filename}.csv",
            "error": None
        }
    
    def generate_pdf_report(self, df: pd.DataFrame, season: str, year: str) -> Dict[str, str]:
        """Generate actual PDF report using ReportLab."""
        if df.empty:
            return {"content": "", "filename": "", "error": "No data to export"}
        
        try:
            # Create PDF in memory
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Prepare content
            elements = []
            
            # Title
            title = Paragraph("Agricultural Production Report", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 12))
            
            # Report details
            details = f"Season: {season if season != 'All' else 'All Seasons'}<br/>Year: {year if year != 'All' else 'All Years'}"
            details_para = Paragraph(details, styles['Normal'])
            elements.append(details_para)
            elements.append(Spacer(1, 20))
            
            # Summary statistics
            stats = self.data_loader.get_summary_stats(season, year)
            summary_data = [
                ['Metric', 'Value'],
                ['Total Area under Production', f"{Formatters.format_number(stats['total_area'])} Hac"],
                ['Total Burned Area', f"{Formatters.format_number(stats['burned_area'])} Hac"],
                ['Total Difference', f"{Formatters.format_number(stats['difference'])} Hac"],
                ['Average % Difference', Formatters.format_percentage(stats['pct_avg'])]
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(Paragraph("Summary Statistics", styles['Heading2']))
            elements.append(Spacer(1, 6))
            elements.append(summary_table)
            elements.append(Spacer(1, 20))
            
            # Data preview
            elements.append(Paragraph("Data Preview (First 10 Records)", styles['Heading2']))
            elements.append(Spacer(1, 6))
            
            # Prepare data for table
            preview_df = df.head(10)
            table_data = [preview_df.columns.tolist()]
            table_data.extend(preview_df.values.tolist())
            
            data_table = Table(table_data)
            data_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            elements.append(data_table)
            
            # Build PDF
            doc.build(elements)
            
            # Get PDF content as base64
            pdf_content = buffer.getvalue()
            b64 = base64.b64encode(pdf_content).decode()
            
            return {
                "content": f"data:application/pdf;base64,{b64}",
                "filename": self.get_export_filename(season, year, "pdf"),
                "error": None
            }
            
        except Exception as e:
            return {"content": "", "filename": "", "error": f"PDF generation error: {str(e)}"}
    
    def create_report_preview_components(self, df: pd.DataFrame, season: str, year: str) -> html.Div:
        """Create Dash components for report preview."""
        stats = self.data_loader.get_summary_stats(season, year)

        # Determine how many records to show
        total_records = len(df)
        if total_records <= 20:
            # Show all records for small datasets
            preview_df = df
            record_text = f"Showing all {total_records} records"
        else:
            # Show first 15 records for larger datasets with scroll
            preview_df = df.head(15)
            record_text = f"Showing first 15 of {total_records} records (scroll for more)"

        # Create table headers
        headers = [html.Th(col, style={"background": "var(--gradient-primary)", "color": "white", "padding": "12px 8px", "textAlign": "left", "fontWeight": "600", "position": "sticky", "top": "0", "zIndex": "10"}) for col in preview_df.columns]

        # Create table rows
        rows = []
        for i, (_, row) in enumerate(preview_df.iterrows()):
            row_style = {"background": "rgba(255, 255, 255, 0.02)" if i % 2 == 0 else "transparent"}
            cells = [html.Td(str(val), style={"padding": "8px", "borderBottom": "1px solid rgba(255, 255, 255, 0.1)", "color": "var(--text-primary)"}) for val in row]
            rows.append(html.Tr(cells, style=row_style))

        return html.Div([
            html.H3("Agricultural Production Report", style={"color": "var(--accent-color)", "marginBottom": "1rem"}),
            html.P([html.Strong("Season: ", style={"color": "var(--text-secondary)"}), season if season != "All" else "All Seasons"]),
            html.P([html.Strong("Year: ", style={"color": "var(--text-secondary)"}), year if year != "All" else "All Years"]),

            html.H4("Summary Statistics", style={"color": "var(--text-secondary)", "margin": "1.5rem 0 0.5rem 0"}),

            html.Table([
                html.Tr([
                    html.Th("Metric", style={"background": "rgba(96, 165, 250, 0.1)", "color": "var(--accent-color)", "padding": "0.75rem", "textAlign": "left", "borderBottom": "1px solid rgba(255, 255, 255, 0.1)"}),
                    html.Th("Value", style={"background": "rgba(96, 165, 250, 0.1)", "color": "var(--accent-color)", "padding": "0.75rem", "textAlign": "left", "borderBottom": "1px solid rgba(255, 255, 255, 0.1)"})
                ])
            ] + [
                html.Tr([
                    html.Td(metric_name, style={"padding": "0.75rem", "borderBottom": "1px solid rgba(255, 255, 255, 0.1)", "color": "var(--text-primary)"}),
                    html.Td(metric_value, style={"padding": "0.75rem", "borderBottom": "1px solid rgba(255, 255, 255, 0.1)", "color": "var(--text-primary)"})
                ]) for metric_name, metric_value in [
                    ("Total Area under Production", f"{Formatters.format_number(stats['total_area'])} Hac"),
                    ("Total Burned Area", f"{Formatters.format_number(stats['burned_area'])} Hac"),
                    ("Total Difference", f"{Formatters.format_number(stats['difference'])} Hac"),
                    ("Average % Difference", Formatters.format_percentage(stats['pct_avg']))
                ]
            ], style={"width": "100%", "borderCollapse": "collapse", "background": "rgba(30, 41, 59, 0.5)", "borderRadius": "8px", "overflow": "hidden"}),

            html.H4("Data Preview", style={"color": "var(--text-secondary)", "margin": "1.5rem 0 0.5rem 0"}),
            html.P(record_text, className="record-count"),
            html.Div(
                html.Table(
                    [html.Tr(headers)] + rows,
                    className="data-preview-table"
                ),
                className="table-container"
            )
        ], className="report-preview-content")

    def _create_report_preview(self, df: pd.DataFrame, season: str, year: str) -> str:
        """Create HTML preview of the report (legacy method for backward compatibility)."""
        stats = self.data_loader.get_summary_stats(season, year)

        # Determine how many records to show
        total_records = len(df)
        if total_records <= 20:
            # Show all records for small datasets
            preview_df = df
            record_text = f"Showing all {total_records} records"
        else:
            # Show first 15 records for larger datasets with scroll
            preview_df = df.head(15)
            record_text = f"Showing first 15 of {total_records} records (scroll for more)"

        preview_html = f"""
        <div class="report-preview-content">
            <h3>Agricultural Production Report</h3>
            <p><strong>Season:</strong> {season if season != 'All' else 'All Seasons'}</p>
            <p><strong>Year:</strong> {year if year != 'All' else 'All Years'}</p>

            <h4>Summary Statistics</h4>
            <table class="report-table">
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Total Area under Production</td><td>{Formatters.format_number(stats['total_area'])} Hac</td></tr>
                <tr><td>Total Burned Area</td><td>{Formatters.format_number(stats['burned_area'])} Hac</td></tr>
                <tr><td>Total Difference</td><td>{Formatters.format_number(stats['difference'])} Hac</td></tr>
                <tr><td>Average % Difference</td><td>{Formatters.format_percentage(stats['pct_avg'])}</td></tr>
            </table>

            <h4>Data Preview</h4>
            <p class="record-count">{record_text}</p>
            <div class="table-container">
                {preview_df.to_html(classes='data-preview-table', index=False)}
            </div>
        </div>
        """

        return preview_html
    
    def get_export_filename(self, season: str, year: str, format_type: str) -> str:
        """Generate appropriate filename for export."""
        season_part = season.lower() if season != "All" else "all_seasons"
        year_part = str(year).lower() if year != "All" else "all_years"

        if format_type == "csv":
            return f"agriculture_data_{season_part}_{year_part}.csv"
        else:
            return f"agriculture_report_{season_part}_{year_part}.pdf"
