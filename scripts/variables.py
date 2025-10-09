from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar


@dataclass(frozen=True)
class BasePaths:
    data_path: Path = Path("./data/")
    raw_path: Path = Path("./data/raw/")
    preprocessed_data_path = Path("./preprocessed/")

    train_raw_name: str = "train_raw.csv"
    test_raw_name: str = "test_raw.csv"

    train_raw_path: Path = raw_path / train_raw_name
    test_raw_path: Path = raw_path / test_raw_name


@dataclass(frozen=True)
class VarEDA(BasePaths):
    train_raw_path: Path = BasePaths.train_raw_path
    test_raw_path: Path = BasePaths.test_raw_path


@dataclass(frozen=True)
class VarPreprocessor(BasePaths):
    train_raw_path: Path = BasePaths.train_raw_path
    test_raw_path: Path = BasePaths.test_raw_path

    train_preprocessed_name: str = "train_preprocessed.csv"
    test_preprocessed_name: str = "test_preprocessed.csv"

    train_preprocessed_path: Path = BasePaths.preprocessed_data_path / train_preprocessed_name
    test_preprocessed_path: Path = BasePaths.preprocessed_data_path / test_preprocessed_name

    encoding_columns: ClassVar[list[str]] = ["Sex", "Embarked"]
