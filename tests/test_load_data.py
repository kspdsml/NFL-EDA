import os
import sys
import pandas as pd
import numpy as np

# Ensure the parent directory is in the path so that `utils` can be imported
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import load_data


def test_load_data_preserves_float_columns(monkeypatch):
    """load_data should keep float columns as floats with correct decimals."""
    sample_df = pd.DataFrame(
        {
            "Rk": [1],
            "Player": ["Test Player"],
            "Age": [25],
            "G": [1],
            "GS": [1],
            "Att": [10],
            "Yds": [100],
            "TD": [1],
            "1D": [5],
            "Lng": [20],
            "Y/A": [5.5],
            "Y/G": [100.5],
            "Fmb": [0],
        }
    )

    monkeypatch.setattr("utils.pd.read_html", lambda *args, **kwargs: [sample_df])

    result = load_data(2020, "rushing")

    for column, value in {"Y/A": 5.5, "Y/G": 100.5}.items():
        assert np.issubdtype(result[column].dtype, np.floating), f"{column} is not float"
        assert result[column].iloc[0] == value
