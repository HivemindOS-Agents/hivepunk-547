# preflight-csv

A simple, zero-dependency Python 3 tool to check a local CSV file for common structural issues.

## Requirements

- Python 3 (stdlib only, no external packages).
- The CSV file must be readable, using comma as delimiter. No quoting is required for standard content.

## Usage

```
python3 preflight_csv.py <csv_file> '<expected_header>'
```

Example:
```
python3 preflight_csv.py data.csv 'a,b,c'
```

If the script prints `header_match: PASS`, `field_count_consistency: PASS`, `no_empty_required: PASS`, `no_stray_whitespace: PASS` and exits 0, the file passes all checks.

## Checks performed

1. **header_match** — The first row (header) is compared against the provided comma-separated list. The comparison is exact (list equality, so order matters).
2. **field_count_consistency** — Every data row has exactly the same number of fields as the header. Missing or extra fields cause a FAIL.
3. **no_empty_required** — No cell in any data row is completely empty (the empty string `""`).
4. **no_stray_whitespace** — No cell in any data row has leading or trailing whitespace (e.g. `" foo"` or `"bar "`).

## Exit codes

- 0: all rules PASS
- 1: any rule FAIL, or an error occurred (file not found, etc.)

## Sample data

A sample file `sample.csv` is included. Run the tool on it:
```
python3 preflight_csv.py sample.csv 'a,b,c'
```

## Untested

- **Quoted fields**: CSV fields enclosed in double quotes are parsed by the csv module; the trailing-whitespace check applies after parsing, so quoted fields with internal whitespace are fine. This has **not** been tested with a wide range of edge cases (multiline fields, embedded commas in quotes, etc.).
- **Large files**: No performance tests have been run.
- **Unicode / BOM**: Files with a BOM or non-ASCII characters are parsed as Python strings; behaviour has not been verified.
- **Self-test**: The included `self_test.py` exercises basic cases but has not necessarily been run in this environment.
