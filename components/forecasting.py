"""
Forecasting Component
Implements ARIMA and Exponential Smoothing for agricultural time series forecasting
"""

import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from utils.data_loader import DataLoader
from utils.formatters import Formatters
import warnings
warnings.filterwarnings('ignore')

try:
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from sklearn.metrics import mean_absolute_error, mean_squared_error
except ImportError:
    print("Warning: statsmodels or scikit-learn not available. Forecasting features will be limited.")

class Forecasting:
    """Handles time series forecasting for agricultural metrics."""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
    
    def prepare_forecast_data(self, season: str, metric: str = 'area') -> pd.DataFrame:
        """Prepare time series data for forecasting."""
        df = self.data_loader.filter_data(season, "All")
        df = df.sort_values("Year")
        
        # Aggregate by year for the selected metric
        if metric == 'area':
            agg_data = df.groupby("Year")["Area under Production (Hac)"].sum().reset_index()
            agg_data.columns = ['Year', 'Value']
        elif metric == 'burned':
            agg_data = df.groupby("Year")["Burned Area (Hac)"].sum().reset_index()
            agg_data.columns = ['Year', 'Value']
        elif metric == 'pct_diff':
            agg_data = df.groupby("Year")["% Difference Numeric"].mean().reset_index()
            agg_data.columns = ['Year', 'Value']
        else:
            raise ValueError("Invalid metric specified")
        
        return agg_data
    
    def exponential_smoothing_forecast(self, data: pd.DataFrame, periods: int = 3) -> Tuple[pd.DataFrame, Dict]:
        """Perform exponential smoothing forecast."""
        try:
            # Prepare time series
            ts = data.set_index('Year')['Value']
            
            # Fit Holt-Winters model (handles trend and seasonality)
            model = ExponentialSmoothing(
                ts, 
                trend='add', 
                seasonal='add', 
                seasonal_periods=min(3, len(ts))  # Small seasonal period for agricultural data
            )
            fitted_model = model.fit()
            
            # Generate forecast
            forecast = fitted_model.forecast(periods)
            
            # Calculate confidence intervals (simplified)
            last_value = ts.iloc[-1]
            std_dev = ts.std()
            lower = forecast - 1.96 * std_dev
            upper = forecast + 1.96 * std_dev
            
            # Create forecast dataframe
            forecast_years = [data['Year'].max() + i + 1 for i in range(periods)]
            forecast_df = pd.DataFrame({
                'Year': forecast_years,
                'Forecast': forecast.values,
                'Lower_CI': lower.values,
                'Upper_CI': upper.values
            })
            
            # Calculate model metrics
            fitted_values = fitted_model.fittedvalues
            mae = mean_absolute_error(ts, fitted_values)
            rmse = np.sqrt(mean_squared_error(ts, fitted_values))
            
            metrics = {
                'mae': mae,
                'rmse': rmse,
                'model_type': 'Exponential Smoothing'
            }
            
            return forecast_df, metrics
            
        except Exception as e:
            print(f"Exponential smoothing error: {e}")
            return self._create_empty_forecast(periods), {'error': str(e)}
    
    def arima_forecast(self, data: pd.DataFrame, periods: int = 3) -> Tuple[pd.DataFrame, Dict]:
        """Perform ARIMA forecast."""
        try:
            # Prepare time series
            ts = data.set_index('Year')['Value']
            
            # Simple ARIMA model (1,1,1) - can be optimized
            model = ARIMA(ts, order=(1, 1, 1))
            fitted_model = model.fit()
            
            # Generate forecast with confidence intervals
            forecast_result = fitted_model.get_forecast(steps=periods)
            forecast = forecast_result.predicted_mean
            conf_int = forecast_result.conf_int()
            
            # Create forecast dataframe
            forecast_years = [data['Year'].max() + i + 1 for i in range(periods)]
            forecast_df = pd.DataFrame({
                'Year': forecast_years,
                'Forecast': forecast.values,
                'Lower_CI': conf_int.iloc[:, 0].values,
                'Upper_CI': conf_int.iloc[:, 1].values
            })
            
            # Calculate model metrics
            fitted_values = fitted_model.fittedvalues
            mae = mean_absolute_error(ts.iloc[1:], fitted_values.iloc[1:])  # Skip first due to differencing
            rmse = np.sqrt(mean_squared_error(ts.iloc[1:], fitted_values.iloc[1:]))
            
            metrics = {
                'mae': mae,
                'rmse': rmse,
                'model_type': 'ARIMA(1,1,1)'
            }
            
            return forecast_df, metrics
            
        except Exception as e:
            print(f"ARIMA forecast error: {e}")
            return self._create_empty_forecast(periods), {'error': str(e)}
    
    def _create_empty_forecast(self, periods: int) -> pd.DataFrame:
        """Create empty forecast dataframe."""
        return pd.DataFrame({
            'Year': [],
            'Forecast': [],
            'Lower_CI': [],
            'Upper_CI': []
        })
    
    def create_forecast_figure(self, historical_data: pd.DataFrame, 
                             forecast_data: pd.DataFrame, 
                             metric_name: str, 
                             season: str) -> go.Figure:
        """Create forecast visualization figure."""
        fig = go.Figure()
        
        # Add historical data
        fig.add_trace(go.Scatter(
            x=historical_data['Year'],
            y=historical_data['Value'],
            name='Historical Data',
            line=dict(color='#60A5FA', width=3),
            mode='lines+markers'
        ))
        
        if not forecast_data.empty:
            # Add forecast line
            fig.add_trace(go.Scatter(
                x=forecast_data['Year'],
                y=forecast_data['Forecast'],
                name='Forecast',
                line=dict(color='#F472B6', width=3, dash='dash'),
                mode='lines+markers'
            ))
            
            # Add confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_data['Year'].tolist() + forecast_data['Year'].tolist()[::-1],
                y=forecast_data['Upper_CI'].tolist() + forecast_data['Lower_CI'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(244, 114, 182, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='95% Confidence Interval',
                showlegend=True
            ))
        
        # Update layout
        metric_titles = {
            'area': 'Area under Production',
            'burned': 'Burned Area', 
            'pct_diff': 'Percentage Difference'
        }
        
        fig.update_layout(
            title=f"{metric_titles[metric_name]} Forecast - {season if season != 'All' else 'All Seasons'}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#0B1730",
            font_color="#E5EEFF",
            margin=dict(t=50, r=20, b=40, l=40),
            xaxis=dict(title="Year"),
            yaxis=dict(title=metric_titles[metric_name]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            showlegend=True
        )
        
        return fig
    
    def create_forecast_card(self):
        """Create the forecasting visualization card."""
        return html.Div(
            className="card forecast-card",
            children=[
                html.H3("Time Series Forecasting", className="card-title"),
                html.Div(
                    className="forecast-controls",
                    children=[
                        html.Label("Select Metric:", className="filter-label"),
                        dcc.Dropdown(
                            id="forecast-metric-dd",
                            options=[
                                {'label': 'Area under Production', 'value': 'area'},
                                {'label': 'Burned Area', 'value': 'burned'},
                                {'label': 'Percentage Difference', 'value': 'pct_diff'}
                            ],
                            value='area',
                            className="dropdown"
                        ),
                        html.Label("Forecast Periods:", className="filter-label"),
                        dcc.Slider(
                            id="forecast-periods-slider",
                            min=1,
                            max=5,
                            step=1,
                            value=3,
                            marks={i: str(i) for i in range(1, 6)},
                            className="slider"
                        ),
                        html.Label("Model Type:", className="filter-label"),
                        dcc.RadioItems(
                            id="forecast-model-radio",
                            options=[
                                {'label': 'Exponential Smoothing', 'value': 'exponential'},
                                {'label': 'ARIMA', 'value': 'arima'}
                            ],
                            value='exponential',
                            className="radio-items"
                        ),
                        html.Button(
                            "Generate Forecast",
                            id="forecast-generate-btn",
                            n_clicks=0,
                            className="forecast-btn"
                        )
                    ]
                ),
                html.Div(
                    className="forecast-results",
                    children=[
                        dcc.Graph(
                            id="forecast-fig",
                            config={'displayModeBar': True},
                            style={"height": "400px"}
                        ),
                        html.Div(
                            id="forecast-metrics",
                            className="forecast-metrics"
                        )
                    ]
                )
            ]
        )
