# PRD — PDF Watermark CLI Tool

## Overview

A Python CLI tool that adds diagonal, tiled, semi-transparent watermarks to PDF files. Each page is rasterized to prevent element extraction or editing, then reassembled into a watermarked PDF.

---

## Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-001 | Accept exactly two positional CLI arguments: full path to input PDF and watermark text string |
| FR-002 | Output a new file in the same directory as the input, named `{original_stem}_watermark.pdf` |
| FR-003 | Rasterize every page of the input PDF to an image before applying the watermark (prevents element copy/edit) |
| FR-004 | Render watermark text diagonally at -45 degrees across each page |
| FR-005 | Tile the watermark so it repeats across the full page without gaps |
| FR-006 | Apply watermark at semi-transparent opacity — visible over content but not obscuring it |
| FR-007 | Preserve the original page dimensions in the output PDF |
| FR-008 | Handle multi-page PDFs correctly — all pages watermarked and reassembled in order |
| FR-009 | Exit with a non-zero status code and a clear error message on invalid inputs (missing file, wrong extension, empty watermark text) |
| FR-010 | Produce output that passes visual inspection: watermark covers the full page, text is legible, original content remains readable |

---

## Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-001 | Processing time ≤ 10 seconds for a standard 10-page A4 PDF on modern hardware |
| NFR-002 | No system-level dependencies beyond Python 3.9+ and pip-installable packages |
| NFR-003 | Single-file implementation (`watermark.py`) — no package structure at MVP scale |
| NFR-004 | Compatible with macOS, Linux, and Windows |
| NFR-005 | Output PDF must be openable by standard PDF viewers (Adobe Acrobat, Preview, Chrome) |

---

## Out of Scope (MVP)

- GUI or web interface
- Batch processing of multiple PDFs in one invocation
- Custom font selection via CLI
- Watermark color or opacity configuration via CLI
- Password-protected PDFs
- Preserving PDF hyperlinks, annotations, or form fields (rasterization intentionally removes these)
- Watermark removal or detection

---

## Success Criteria

The tool is considered complete when:

1. Running `python watermark.py /path/to/file.pdf "CONFIDENTIAL"` produces `file_watermark.pdf` in the same directory
2. Every page of the output contains a tiled diagonal watermark covering the full page
3. The watermark is visible but the original content (text, images) remains legible underneath
4. The output file opens without error in at least two standard PDF viewers
5. Invalid inputs (bad path, non-PDF file, empty text) produce a clear error message and non-zero exit code
6. Processing a 10-page A4 PDF completes in under 10 seconds
