# Milestones — PDF Watermark CLI Tool

Living checklist. Mark each task `[x]` when complete before moving to the next milestone.

---

## M1 — Project Setup & Dependency Validation

**Goal**: Working environment with all dependencies installed and importable.

- [x] Create `requirements.txt` with `PyMuPDF>=1.23.0` and `Pillow>=10.0.0`
- [x] Create skeleton `watermark.py` with placeholder functions and `main()` entry point
- [x] Verify `import fitz` and `from PIL import Image` succeed without errors
- [x] Verify `fitz.open("sample/test.pdf")` opens without error and `len(doc) > 0`
- [x] Confirm `argparse` parses two positional arguments correctly (dry run with `--help`)

**Done when**: `python watermark.py --help` shows usage, and all imports succeed.

---

## M2 — Page Rasterization

**Goal**: Each PDF page converts to a correctly-sized RGBA PIL image.

- [x] Implement `rasterize_page(page)` using `fitz.Matrix(DPI/72, DPI/72)` at `DPI=200`
- [x] Verify output image mode is `RGBA`
- [x] Verify image dimensions match expected pixel size for an A4 page at 200 DPI (~1654 × 2339 px)
- [x] Save one rasterized page as a PNG and visually confirm it matches the PDF content
- [x] Handle multi-page PDF: confirm loop produces one image per page

**Done when**: `rasterize_page()` returns a correct RGBA image for every page of `sample/test.pdf`.

---

## M3 — Watermark Overlay

**Goal**: A tiled diagonal watermark overlay is visually correct before integration.

- [x] Implement `make_watermark_overlay(width, height, text)` with oversized canvas rotation strategy
- [x] Implement `apply_watermark(page_img, overlay)` using `alpha_composite`
- [x] Verify overlay is `RGBA` mode and same dimensions as page image
- [x] Visual check: save a composited page as PNG and confirm:
  - [x] Watermark text is at -45 degree angle
  - [x] Watermark tiles cover the full page (no uncovered corners)
  - [x] Original page content is visible underneath
  - [x] Watermark opacity is semi-transparent (not solid, not invisible)
- [x] Verify font size scales correctly: larger page → larger text

**Done when**: A composited PNG of one page passes all visual checks above.

---

## M4 — CLI Integration & End-to-End Test

**Goal**: Full pipeline works from command line; all PRD criteria satisfied.

- [x] Implement `validate_inputs(pdf_path, watermark_text)` with correct error messages and exit codes
- [x] Implement `build_output_path(pdf_path)` returning `{stem}_watermark.pdf`
- [x] Implement `main()` tying together the full pipeline with `argparse`
- [x] E2E test: `python watermark.py sample/test.pdf "CONFIDENTIAL"` produces `sample/test_watermark.pdf`
- [x] Verify output PDF opens in at least two viewers (e.g., Preview + Chrome)
- [x] Verify all pages are present in correct order
- [x] Error handling tests:
  - [x] Missing file → clear error, exit code 1
  - [x] Non-PDF extension → clear error, exit code 1
  - [x] Empty watermark text → clear error, exit code 1
- [x] Performance check: 10-page PDF completes in under 10 seconds
- [x] Final visual inspection: watermark passes all M3 visual checks on full output PDF

**Done when**: All checklist items above are checked and `sample/test_watermark.pdf` passes visual inspection.
