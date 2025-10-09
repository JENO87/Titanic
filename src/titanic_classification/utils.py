from pathlib import Path

import pandas as pd


def load_data(input_dir: Path) -> pd.DataFrame:
    return pd.read_csv(input_dir)
