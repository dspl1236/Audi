# Build Instructions (Reproducible)

This folder contains a reproducible **build spec** for generating the PDF manual from the spreadsheet.

## Files
- `buildspec.json` — declarative parameters for layout, styling, and sections.
- `build_local.py` — Python script that reads the Excel and emits the PDF (single-column, Audi-red headers).
- `Makefile` — convenience targets for local builds.
- `.github/workflows/build-manual.yml` — optional CI job to rebuild on push (requires Python deps).

## Quick Start (local)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install reportlab pandas openpyxl xlsxwriter

# Build using spec
python build/build_local.py --spec build/buildspec.json
```

The output PDF will be written to the path specified in `inputs.pdf_output` (currently:
`aan-3b-b3-repin-guide/spec/AAN_to_3B_B3_7A_Repin_Guide_Full_Manual.pdf`).

## Make Targets
```bash
make build     # build the PDF from buildspec.json
make clean     # remove generated PDFs
```

## CI (GitHub Actions)
If you commit the workflow under `.github/workflows/build-manual.yml`, each push to `main` will rebuild the manual
and publish it as an artifact.

## Notes
- The `appendix_*` sections require the spreadsheet to include the corresponding sheets or will show placeholder tables.
- Verification checkboxes are visual (printable) and non-interactive by design.
- Page numbers are intentionally minimal (TOC + Appendices).
