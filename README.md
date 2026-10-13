# MP1 End-to-End Data Pipeline

This project is a comman -line data pipeline that loads a CSV file, validates it, cleans it, and saves the cleaned result. 


Data moves through the pipeline in order: `pipeline.py` parses the arguments, checks that the input and config paths are files, loads both, validates the DataFrame, cleans it, and saves it to the output path. Everything that depends on the dataset (required columns, numeric columns, and which cleaning steps to run) is controlled by `config/config.yaml`, so the code does not change for a new compatible CSV file. `pipeline.py` coordinates the workflow and decides when to exit, while the reusable code lives in the `src/` package. `src/utils.py` sets up logging and validates input paths, `src/data_loaders.py` loads CSV, JSON, and YAML files, `src/data_validator.py` checks required columns and removes rows with invalid numeric values, `src/data_processor.py` removes duplicates, missing values, and outliers and builds the cleaning report, and `src/data_output.py` saves the result as CSV. Each module logs through its own logger and raises exceptions when something is wrong, and `pipeline.py` catches them and exits with status code 1. Test files are in `fixtures/`, and generated results go to `output/`, which is not committed to Git.

## My set up

```bash
python -m venv venv
source venv/bin/activate        
pip install -r requirements.txt
```

## Example

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```text
02:51:23 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
02:51:23 INFO     src.utils — Input file validated: fixtures/sample_data.csv
02:51:23 INFO     src.utils — Input file validated: config/config.yaml
02:51:23 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
02:51:23 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
02:51:23 WARNING  src.data_validator — Invalid numeric value in rating at row 94: 'not_available'
02:51:23 WARNING  src.data_validator — Invalid numeric value in rating at row 95: 'error'
02:51:23 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
02:51:23 DEBUG    src.data_validator — Validation: 100 -> 98 rows (valid=98, removed=2)
02:51:23 INFO     __main__ — Validation complete: 100 -> 98 rows
02:51:23 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
02:51:23 DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
02:51:23 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
02:51:23 INFO     __main__ — Processing complete: 98 -> 92 rows
02:51:23 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
02:51:23 INFO     __main__ — Saved cleaned data to output/clean.csv

Cleaning report:
{'rows_before': 98,
 'rows_after': 92,
 'rows_removed': 6,
 'columns_before': 5,
 'columns_after': 5,
 'columns_removed': 0}
```
