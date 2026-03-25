# Report export instructions (no binary files in PR)

Some Git hosting/review tools reject pull requests containing binary files (like `.docx`) in the diff view.

To avoid PR creation errors, this repository keeps only:
- Source report content (`docs/final_year_project_report.md`)
- Export script (`scripts/generate_word_report.py`)

## Generate the Word file locally

Run:

```bash
python scripts/generate_word_report.py
```

This generates:

- `docs/IGNOU_MCA_Project_Report_BuyNow.docx`

The `.docx` file is intentionally ignored from git tracking, so it will not block PR creation.

## Suggested submission workflow

1. Commit only source files (`.md`, `.py`).
2. Create PR.
3. Generate `.docx` locally after pulling latest code.
4. Submit `.docx` to college/guide by email or cloud drive.
