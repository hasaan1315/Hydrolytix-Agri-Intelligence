"""
Global configuration settings for the dashboard.
"""

# App Configuration
APP_TITLE = "Hydrolytix • Agri Intelligence"
DEBUG_MODE = True
PORT = 8050

# Data Configuration
DATA_FILE = "agri_analysis_punjab_clean.csv"
DEFAULT_SEASON = "All"
DEFAULT_YEAR = "All"

# Layout Configuration
GRID_BREAKPOINTS = {
    "mobile": 768,
    "tablet": 1024,
    "desktop": 1200
}

# Animation Settings
ANIMATION_DURATION = 300
TRANSITION_DURATION = 200

# Chart Configuration
CHART_HEIGHT = 400
CHART_MARGIN = dict(t=20, r=20, b=40, l=40)
