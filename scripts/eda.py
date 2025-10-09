"""A script for Exploratory Data Analysis."""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace as argparseNamespace
from pathlib import Path

from loguru import logger
from variables import VarEDA

from titanic_classification import PROJECT_NAME, PROJECT_VERSION
from titanic_classification.eda import EDA


def parse_args() -> argparseNamespace:
    """Parsing command line strings into Python objects."""
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=f"Options for {PROJECT_NAME}",
    )

    parser.add_argument(
        "--train-input-dir",
        type=Path,
        default=VarEDA.train_raw_path,
        help="Path to the training data",
    )

    parser.add_argument(
        "--test-input-dir",
        type=Path,
        default=VarEDA.test_raw_path,
        help="Path to the test data",
    )

    return parser.parse_args()


def main(arguments: argparseNamespace) -> None:
    """The main function for downloading data."""
    logger.info("Starting EDA script")
    logger.add("eda.log", format="{time} {level} {message}", level="INFO")

    logger.info("Instantiate EDA class")

    eda = EDA(train_path=arguments.train_path, test_path=arguments.test_path)

    """Run full EDA pipeline."""

    logger.info("Running EDA pipeline...")

    logger.info("Missing Value Summary:")
    logger.info(eda.summarize_missing())
    eda.basic_statistics()
    eda.plot_distributions()
    eda.analyze_categorical()
    logger.info("\nTransformation Suggestions:")
    for feature, suggestion in eda.suggest_transformations().items():
        logger.info(f"{feature}: {suggestion}")

    logger.info(f"Using package {PROJECT_NAME} with version {PROJECT_VERSION}")

    logger.info(f"Input parameters: {vars(arguments)}")


if __name__ == "__main__":
    main(parse_args())
