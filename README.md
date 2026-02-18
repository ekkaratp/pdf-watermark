# pdf-watermark

A Python CLI tool that adds diagonal, tiled, semi-transparent watermarks to PDF files. Each page is **rasterized** before watermarking, preventing element extraction or editing in the output.

## Features

- Diagonal (-45°) tiled watermark covering the full page
- Semi-transparent overlay — visible over content without obscuring it
- Page rasterization locks down the PDF (no copy/paste of original elements)
- Multi-page PDF support — all pages watermarked and reassembled in order
- Output dimensions match the original page size
- Cross-platform: macOS, Linux, Windows

## Requirements

- Python 3.9+
- [PyMuPDF](https://pymupdf.readthedocs.io/) ≥ 1.23.0
- [Pillow](https://pillow.readthedocs.io/) ≥ 10.0.0

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python watermark.py <pdf_path> <watermark_text>
```

**Arguments**

| Argument | Description |
|---|---|
| `pdf_path` | Full path to the input PDF file |
| `watermark_text` | Text string to render as the watermark |

**Output**

The watermarked PDF is written to the same directory as the input, with `_watermark` appended to the filename:

```
report.pdf → report_watermark.pdf
```

**Examples**

```bash
python watermark.py /docs/report.pdf "CONFIDENTIAL"
python watermark.py sample/test.pdf "INTERNAL USE ONLY"
```

## Error Handling

| Condition | Behaviour |
|---|---|
| File not found | Prints error to stderr, exits with code 1 |
| Not a `.pdf` file | Prints error to stderr, exits with code 1 |
| Empty watermark text | Prints error to stderr, exits with code 1 |

## Configuration

All visual parameters are module-level constants in `watermark.py`:

| Constant | Default | Description |
|---|---|---|
| `DPI` | `200` | Rasterization resolution |
| `WATERMARK_OPACITY` | `25` | Alpha value (0–255); 25 ≈ 10% opacity |
| `WATERMARK_COLOR` | `(64, 64, 64)` | Watermark text colour (dark gray) |
| `WATERMARK_ANGLE` | `-45` | Rotation angle in degrees |
| `FONT_SIZE_RATIO` | `0.04` | Font size as a fraction of page width |
| `FONT_SIZE_MIN` | `36` | Minimum font size regardless of page size |
| `TILE_PADDING` | `120` | Pixel gap between watermark tiles |

## How It Works

```
Input PDF
  │
  ├─ validate_inputs()        — path exists, is PDF, text non-empty
  ├─ fitz.open()              — open with PyMuPDF
  │
  └─ for each page:
       rasterize_page()       — render to RGBA image at DPI resolution,
       │                        composited onto a white canvas
       make_watermark_overlay() — tiled diagonal text on transparent RGBA layer
       apply_watermark()      — alpha_composite → convert to RGB
  │
  └─ Pillow save_all=True     — reassemble pages into output PDF
```

The tiling strategy uses an oversized square canvas (side = page diagonal) to ensure rotation never clips content at the corners. The centre crop is then extracted at the exact page dimensions.

## Project Structure

```
pdf-watermark/
├── watermark.py       # Single-file implementation (~150 LOC)
├── requirements.txt   # PyMuPDF + Pillow
├── sample/
│   └── test.pdf       # Test file for manual verification
└── docs/
    ├── PRD.md          # Product requirements
    ├── architecture.md # Design decisions and function contracts
    └── milestones.md   # Development checklist
```

## Out of Scope (MVP)

- GUI or web interface
- Batch processing of multiple PDFs in one invocation
- CLI flags for font, colour, or opacity
- Password-protected PDFs
- Preserving hyperlinks, annotations, or form fields (rasterization intentionally removes these)
