from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class EDA:
    def __init__(self, train_path: Path, test_path: Path):
        self.train: pd.DataFrame = pd.read_csv(train_path)
        self.test: pd.DataFrame = pd.read_csv(test_path)
        self.missing_summary: pd.DataFrame | None = self.summarize_missing()

    def summarize_missing(self) -> pd.DataFrame:
        """Summarize missing values in train and test datasets."""
        self.missing_summary = pd.DataFrame(
            {
                "Train_Missing": self.train.isnull().sum(),
                "Test_Missing": self.test.isnull().sum(),
                "Train_Percent": (self.train.isnull().sum() / len(self.train) * 100).round(2),
                "Test_Percent": (self.test.isnull().sum() / len(self.test) * 100).round(2),
            }
        )
        if self.missing_summary is None:  # Safety check (though unlikely)
            raise ValueError("Failed to create missing summary DataFrame")
        return self.missing_summary

    def basic_statistics(self) -> None:
        """Display basic statistics for numerical features."""
        numeric_cols = ["Age", "SibSp", "Parch", "Fare"]
        print("Basic Statistics for Numerical Features:")
        print(self.train[numeric_cols].describe())
        print("\nSurvival Rate:")
        print(self.train["Survived"].value_counts(normalize=True))

    def plot_distributions(self) -> None:
        """Plot distributions of numerical features."""
        numeric_cols = ["Age", "SibSp", "Parch", "Fare"]
        for col in numeric_cols:
            plt.figure(figsize=(10, 5))
            sns.histplot(data=self.train, x=col, hue="Survived", kde=True)
            plt.title(f"Distribution of {col} by Survival")
            plt.show()

    def analyze_categorical(self) -> None:
        """Analyze categorical features (Pclass, Sex, Embarked)."""
        cat_cols = ["Pclass", "Sex", "Embarked"]
        for col in cat_cols:
            print(f"\nValue Counts for {col}:")
            print(self.train[col].value_counts())
            plt.figure(figsize=(10, 5))
            sns.countplot(data=self.train, x=col, hue="Survived")
            plt.title(f"Survival by {col}")
            plt.show()

    def suggest_transformations(self) -> dict[str, str]:
        """Suggest transformations based on EDA results.

        Ensures missing_summary is populated and provides clear suggestions.
        """
        # Ensure missing_summary is populated (should always be due to __init__)
        if self.missing_summary is None:
            raise RuntimeError("Missing summary failed to initialize")

        suggestions = {}
        # Fare: Check skewness
        fare_skew = self.train["Fare"].skew()
        suggestions["Fare"] = f"Skewness: {fare_skew:.2f}. Consider log-transformation if > 1."  # type: ignore[str-bytes-safe]

        # Cabin: High missingness
        cabin_missing_percent = str(self.missing_summary.loc["Cabin", "Train_Percent"])
        if pd.isna(cabin_missing_percent):
            cabin_missing_percent = "0.0"
        suggestions["Cabin"] = f"Missing: {cabin_missing_percent}%. Consider deck extraction or missing flag."

        # Age: Missingness
        age_missing_percent = str(self.missing_summary.loc["Age", "Train_Percent"])
        if pd.isna(age_missing_percent):
            age_missing_percent = "0.0"
        suggestions["Age"] = f"Missing: {age_missing_percent}%. Consider median imputation."

        return suggestions

    def run_eda(self) -> None:
        """Run full EDA pipeline."""
        print("Missing Value Summary:")
        print(self.summarize_missing())
        self.basic_statistics()
        self.plot_distributions()
        self.analyze_categorical()
        print("\nTransformation Suggestions:")
        for feature, suggestion in self.suggest_transformations().items():
            print(f"{feature}: {suggestion}")
