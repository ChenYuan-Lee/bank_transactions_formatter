# Bank Transactions Formatter

1. Install [poetry](https://python-poetry.org/docs/)
2. Run `poetry install` (see [docs](https://python-poetry.org/docs/basic-usage/#installing-with-poetrylock)). This creates a `.venv` folder in the root directory.
3. The Python interpreter (of the IDE/project) can now be configured to use that of this `.venv`.
4. Create 2 folders in the root directory: `input_files` & `output_files`
    * Place the downloaded transaction-history or e-statement files into the `input_files` folder
5. Run `main.py`


## Files Download Procedure

### DBS Credit Card
1. View transaction history
2. Copy transactions from website and paste into `dbs_statement.txt`


## TODOs
1. Use logging instead of print
2. Use enum (with @unique) to define file names to detect name collision