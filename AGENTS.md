# openarch

Repository for consulting architecture regulations and technical documentation (CTE, GVA regulations, etc.).

## Documentation

All regulation documents are in the `documents/` folder, converted to TXT format for easy searching and reading.

- CTE (Spanish Technical Building Code): SE, SI, SUA, HE, HR, HS
- GVA regional regulations

## Document updater

Documents are managed with the `scripts/doc-updater/update.py` script, which reads the configuration from `scripts/doc-updater/documents.yml`.

`documents.yml` contains the list of documents with:
- `local`: path to the .txt file (relative to the project root)
- `url`: link to the original PDF
- `last_modified`: last modification date from the server (updated automatically)

The script compares the server's `Last-Modified` date with the stored one. If there are changes, it downloads the PDF, converts it to TXT, and updates the date in the YAML.

```bash
source .venv/bin/activate && python3 scripts/doc-updater/update.py
```

## Python tools

When you need to read or edit Word (.docx) or Excel (.xlsx) files, use Python with the `python-docx` and `openpyxl` libraries.

Before running Python scripts, create a virtual environment and install the required dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install python-docx openpyxl requests pyyaml
```

Always run scripts from the project root using the virtual environment:

```bash
source .venv/bin/activate && python3 script.py
```
