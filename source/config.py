from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

# Data Path
# =========
PATH_TO_DATA = PROJECT / "data/San_Francisco_2016_.csv"

# Seed for reproducibility
# ========================
SEED = 42

# San Francisco latitude & longitude
LATITUDE, LONGITUDE = 37.77, -122.42
