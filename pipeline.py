"""
Data Processing Pipeline

DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
"""

import argparse
import logging
import sys
from pprint import pprint

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Command-line data pipeline: load, validate, clean, and save data"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input file"
    )
    parser.add_argument(
        "--config", "-c",
        required=True,
        help="Path to the YAML configuration file"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to the output CSV file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose (DEBUG) logging"
    )
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(
        f"Arguments parsed: input={args.input}, config={args.config}, "
        f"output={args.output}"
    )

    # Validate both files BEFORE calling any loader
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # Load the input data and the configuration
    try:
        df = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # Read the validation settings from the config
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    # Validate the DataFrame
    rows_before_validation = len(df)
    try:
        df = validate_dataframe(df, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info(f"Validation complete: {rows_before_validation} -> {len(df)} rows")

    # Keep a copy of the validated data so we can compare before/after
    df_original = df.copy()

    # Process the data
    try:
        df_clean = process_data(df, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_original, df_clean)
    logger.info(f"Processing complete: {len(df_original)} -> {len(df_clean)} rows")

    # Save the output
    save_data(df_clean, args.output)
    logger.info(f"Saved cleaned data to {args.output}")

    # Print the report last
    print("\nCleaning report:")
    pprint(report, sort_dicts=False)


if __name__ == "__main__":
    main()
