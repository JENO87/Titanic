"""A script for Exploratory Data Analysis."""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace as argparseNamespace
from pathlib import Path

from loguru import logger
from variables import VarPreprocessor

from titanic_classification import PROJECT_NAME, PROJECT_VERSION
from titanic_classification.preprocessor import Preprocessor
from titanic_classification.utils import load_data


def parse_args() -> argparseNamespace:
    """Parsing command line strings into Python objects."""
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=f"Options for {PROJECT_NAME}",
    )

    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=f"Options for {PROJECT_NAME}",
    )

    parser.add_argument(
        "--train-input-dir",
        type=Path,
        default=VarPreprocessor.train_raw_path,
        help="Input path to the training data",
    )

    parser.add_argument(
        "--test-input-dir",
        type=Path,
        default=VarPreprocessor.test_raw_path,
        help="Input path to the test data",
    )

    parser.add_argument(
        "--preprocessed-train-output-dir",
        type=Path,
        default=VarPreprocessor.train_preprocessed_path,
        help="Output path for the preprocessed train data",
    )

    parser.add_argument(
        "--preprocessed-test-output-dir",
        type=Path,
        default=VarPreprocessor.test_preprocessed_path,
        help="Output path for the preprocessed test data",
    )

    return parser.parse_args()


def main(arguments: argparseNamespace) -> None:
    """The main function for downloading data."""
    logger.info("Starting preprocessing script...")
    logger.add("preprocess.log", format="{time} {level} {message}", level="INFO")

    logger.info("Instantiate preprocessor class")

    train_data = load_data(arguments.train_input_dir)
    test_data = load_data(arguments.test_input_dir)

    """Run full preprocess pipeline."""

    logger.info("Running preprocessing pipeline...")

    preprocessor = Preprocessor(encoding_columns=VarPreprocessor.encoding_columns)
    train_data, val_data = preprocessor.train_val_split(data=train_data, validation_size=0.2)

    logger.info(f"Training data after split: {train_data.head()}")
    logger.info(f"Validation data after split: {val_data.head()}")

    preprocessor.fit_encoder(train_data)
    train_preprocessed = (
        preprocessor.drop_cabin(train_data)
        .pipe(preprocessor.drop_non_predictive)
        .pipe(preprocessor.impute_age)
        .pipe(preprocessor.impute_fare)
        .pipe(preprocessor.log_fare)
        .pipe(preprocessor.create_family_size)
        .pipe(preprocessor.encode_categoricals)
    )
    val_preprocessed = (
        preprocessor.drop_cabin(val_data)
        .pipe(preprocessor.drop_non_predictive)
        .pipe(preprocessor.impute_age)
        .pipe(preprocessor.impute_fare)
        .pipe(preprocessor.log_fare)
        .pipe(preprocessor.create_family_size)
        .pipe(preprocessor.encode_categoricals)
    )
    test_preprocessed = (
        preprocessor.drop_cabin(test_data)
        .pipe(preprocessor.drop_non_predictive)
        .pipe(preprocessor.impute_age)
        .pipe(preprocessor.impute_fare)
        .pipe(preprocessor.log_fare)
        .pipe(preprocessor.create_family_size)
        .pipe(preprocessor.encode_categoricals)
    )

    logger.info("Finished preprocessing pipeline.")
    logger.info("Processed Train Data:")
    logger.info(train_preprocessed.head())
    logger.info("Processed Val Data:")
    logger.info(val_preprocessed.head())
    logger.info("\nProcessed Test Data:")
    logger.info(test_preprocessed.head())

    logger.info(f"Using package {PROJECT_NAME} with version {PROJECT_VERSION}")

    logger.info(f"Input parameters: {vars(arguments)}")


if __name__ == "__main__":
    main(parse_args())
