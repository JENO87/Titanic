from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BasePaths:
    raw_data_path: Path = Path('./data/')
    processed_data_path: Path = Path('./processed/')
    train_data_name: str = 'train.csv'
    test_data_name: str = 'test.csv'

    train_path: Path = raw_data_path / train_data_name
    test_path: Path = raw_data_path / test_data_name
