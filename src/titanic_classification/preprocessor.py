import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


class Preprocessor:
    def __init__(self, encoding_columns: list[str]):
        self.encoder = OneHotEncoder(drop="first")
        self.encoding_columns = encoding_columns

    def train_val_split(
        self, data: pd.DataFrame, validation_size: float = 0.2, random_state: int = 42
    ) -> tuple[DataFrame, DataFrame]:
        """Split raw train data and preprocess each split separately.

        Args:
            data: raw training data
            validation_size (float): Proportion for validation (default 0.2).
            random_state (int): Seed for reproducibility.
        Returns: None, saves processed files.
        Rationale: Fits preprocessor on train split only to avoid validation leakage.
        """
        # Split first
        X = data.drop(columns=["Survived"])
        y = data["Survived"]
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_size, random_state=random_state, stratify=y
        )
        train_data = pd.concat([X_train, y_train], axis=1)
        val_data = pd.concat([X_val, y_val], axis=1)

        return train_data, val_data

    """Drop columns with a lot of missing values"""

    def drop_cabin(self, data: pd.DataFrame) -> pd.DataFrame:
        """Drop the Cabin column due to high missingness.

        Args: pd.DataFrame with 'Cabin' column.
        Returns: pd.DataFrame without 'Cabin' column.
        Rationale: ~77% missing values, insufficient data for imputation or feature extraction with small
        dataset (891 train, 418 test).
        """
        data_copy = data.copy()
        return data_copy.drop(columns=["Cabin"])

    def drop_non_predictive(self, data: pd.DataFrame) -> pd.DataFrame:
        """Drop non-predictive columns (Name, Ticket, PassengerId for train).

        Args: pd.DataFrame with non-predictive columns.
        Returns: pd.DataFrame without non-predictive columns.
        Rationale: Name and Ticket lack predictive power; PassengerId is an index.
        """
        data_copy = data.copy()
        columns_to_drop = ["Name", "Ticket"]
        if "PassengerId" in data_copy.columns:  # Keep for test submission
            columns_to_drop.append("PassengerId")
        return data_copy.drop(columns=columns_to_drop)

    """Feature engineering"""

    def impute_age(self, data: pd.DataFrame) -> pd.DataFrame:
        """Impute missing Age values with the median age.

        Args: pd.DataFrame with 'Age' column.
        Returns: pd.DataFrame with imputed 'Age' values.
        Rationale: ~20% missing, median avoids outlier skew (max 80).
        """
        age_median = None

        data_copy = data.copy()
        if age_median is None:
            age_median = data_copy["Age"].median()
        data_copy["Age"] = data_copy["Age"].fillna(age_median)
        return data_copy

    def impute_fare(self, data: pd.DataFrame) -> pd.DataFrame:
        """Impute missing Fare values with the median fare.

        Args: pd.DataFrame with 'Fare' column.
        Returns: pd.DataFrame with imputed 'Fare'.
        Rationale: ~0.24% missing in test, median is robust for small missingness.
        """
        fare_median = None

        data_copy = data.copy()
        if fare_median is None:
            fare_median = data_copy["Fare"].median()
        data_copy["Fare"] = data_copy["Fare"].fillna(fare_median)
        return data_copy

    def log_fare(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply log-transformation to Fare to reduce skewness.

        Args: pd.DataFrame with 'Fare' column.
        Returns: pd.DataFrame with log-transformed 'Fare'.
        Rationale: Skewness 4.79, log1p handles zero/near-zero values and normalizes distribution.
        """
        data_copy = data.copy()
        data_copy["Fare"] = np.log1p(data_copy["Fare"])  # log1p for stability with 0 values
        return data_copy

    def create_family_size(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create FamilySize feature from SibSp and Parch.

        Args: pd.DataFrame with 'SibSp' and 'Parch' columns.
        Returns: pd.DataFrame with 'FamilySize' column.
        Rationale: Combines siblings/spouses and parents/children (+1 for passenger) to capture family impact.
        """
        data_copy = data.copy()
        data_copy["FamilySize"] = data_copy["SibSp"] + data_copy["Parch"] + 1
        return data_copy

    def fit_encoder(self, data: pd.DataFrame) -> None:
        """Fit the OneHotEncoder on the training data.

        Args: pd.DataFrame with 'Sex' and 'Embarked' columns.
        Returns: None, updates self.encoder.
        Rationale: Fits encoder on train to avoid data leakage to test.
        """
        self.encoder.fit(data[self.encoding_columns])

    def encode_categoricals(self, data: pd.DataFrame) -> pd.DataFrame:
        """One-hot encode Sex and Embarked columns.

        Args: pd.DataFrame with 'Sex' and 'Embarked' columns.
        Returns: pd.DataFrame with encoded categorical columns.
        Rationale: Converts categorical variables to numerical for modeling, dropping first category to
        avoid multicollinearity.
        """
        data_copy = data.copy()
        # Ensure Sex and Embarked are present for encoding
        if "Sex" not in data_copy.columns or "Embarked" not in data_copy.columns:
            raise ValueError("Sex and Embarked must be present for encoding or fitted earlier.")
        encoded_cols = self.encoder.transform(data_copy[self.encoding_columns])
        encoded_data = pd.DataFrame(encoded_cols, columns=self.encoder.get_feature_names_out())
        data_copy = pd.concat([data_copy, encoded_data], axis=1).drop(columns=["Sex", "Embarked"])
        return data_copy
