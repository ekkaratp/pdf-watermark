# Architecture — PDF Watermark CLI Tool

## Overview

Single-file implementation (`watermark.py`, ~150 LOC). No package structure at MVP scale.

---

## Dependencies

```
PyMuPDF>=1.23.0   # PDF parsing and page rasterization
Pillow>=10.0.0    # RGBA compositing, TTF font rendering, PDF assembly
```

---

## Configuration Constants

All tunable parameters are defined as module-level constants at the top of `watermark.py`:

```python
DPI = 200                          # Rasterization resolution (quality/performance balance)
WATERMARK_OPACITY = 25             # Alpha value 0–255; 25 ≈ 10% opacity (light, non-intrusive)
WATERMARK_COLOR = (64, 64, 64)     # Dark gray — professional, neutral
WATERMARK_ANGLE = -45              # Degrees; standard diagonal direction
FONT_SIZE_RATIO = 0.04             # Font size = max(36, page_width_px * ratio)
FONT_SIZE_MIN = 36                 # Minimum font size regardless of page dimensions
TILE_PADDING = 120                 # Pixels between watermark text tiles (wider for bold letterforms)
```

---

## Processing Pipeline

```
Input: pdf_path (str), watermark_text (str)
  │
  ├─ validate_inputs(pdf_path, watermark_text)
  │     raises SystemExit with message on error
  │
  ├─ fitz.open(pdf_path)
  │
  ├─ for each page:
  │     rasterize_page(page) → PIL Image (RGBA)
  │     make_watermark_overlay(width, height, watermark_text) → PIL Image (RGBA)
  │     apply_watermark(page_img, overlay) → PIL Image (RGB)
  │
  ├─ output_pages[0].save(
  │     output_path,
  │     save_all=True,
  │     append_images=output_pages[1:]
  │   )
  │
Output: {stem}_watermark.pdf (same directory as input)
```

---

## Function Contracts

### `validate_inputs(pdf_path: str, watermark_text: str) -> None`

Validates CLI arguments before any processing begins.

- Raises `SystemExit` (code 1) with a descriptive message if:
  - `pdf_path` does not exist on the filesystem
  - `pdf_path` does not have a `.pdf` extension (case-insensitive)
  - `watermark_text` is empty or whitespace-only
- Returns `None` on success

### `rasterize_page(page: fitz.Page) -> PIL.Image.Image`

Converts a single PDF page to a PIL image at the configured DPI.

- Uses `fitz` matrix scaling: `fitz.Matrix(DPI/72, DPI/72)`
- Returns an RGBA PIL image
- Page dimensions are preserved at the scaled resolution

### `make_watermark_overlay(width: int, height: int, text: str) -> PIL.Image.Image`

Creates a fully transparent RGBA image of the given dimensions with tiled diagonal watermark text.

**Tiling algorithm:**
1. Create a transparent RGBA canvas at `(width, height)`
2. Calculate font size: `max(FONT_SIZE_MIN, int(width * FONT_SIZE_RATIO))`
3. Load a TTF font (Pillow built-in fallback acceptable for MVP)
4. Measure text bounding box using `font.getbbox(text)`
5. Create a temporary oversized canvas (diagonal length × diagonal length) to allow rotation without clipping
6. Tile the text across this canvas with `TILE_PADDING` spacing
7. Rotate the canvas by `WATERMARK_ANGLE` degrees (expand=False on oversized canvas)
8. Crop the center `(width, height)` region from the rotated canvas
9. Return the cropped overlay

### `apply_watermark(page_img: PIL.Image.Image, overlay: PIL.Image.Image) -> PIL.Image.Image`

Composites the watermark overlay onto the page image.

- Both inputs must be RGBA mode
- Uses `PIL.Image.alpha_composite(page_img, overlay)`
- Converts result to RGB before returning (removes alpha channel for PDF assembly)
- Returns RGB PIL image

### `build_output_path(pdf_path: str) -> str`

Derives the output file path from the input path.

- Returns `{parent_dir}/{stem}_watermark.pdf`
- Example: `/docs/report.pdf` → `/docs/report_watermark.pdf`

### `main() -> None`

Entry point. Orchestrates the full pipeline.

- Parses CLI arguments using `argparse`
- Calls `validate_inputs()`
- Opens PDF with `fitz`
- Loops over pages: rasterize → overlay → composite
- Saves assembled output PDF
- Prints success message to stdout

---

## CLI Interface

```
usage: watermark.py [-h] pdf_path watermark_text

positional arguments:
  pdf_path        Full path to the input PDF file
  watermark_text  Text to use as the watermark

optional arguments:
  -h, --help      show this help message and exit
```

---

## Error Handling

| Condition | Behavior |
|-----------|----------|
| File not found | Print error to stderr, exit code 1 |
| Not a PDF | Print error to stderr, exit code 1 |
| Empty watermark text | Print error to stderr, exit code 1 |
| Unexpected runtime error | Allow Python default traceback (not an MVP concern) |

---

## Output

- File: `{input_stem}_watermark.pdf` in the same directory as the input
- Format: PDF assembled from JPEG-compressed page images via Pillow's `save_all=True`
- All pages present in original order
