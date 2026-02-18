# Technical Decisions — PDF Watermark CLI Tool

Decision log for all significant technical choices. Each entry documents the decision, alternatives considered, and rationale.

---

## TD-001 — Programming Language: Python 3.9+

**Decision**: Implement in Python 3.9+.

**Alternatives considered**:
- Node.js
- Go

**Rationale**: Specified in the project spec. Python has the strongest ecosystem for PDF and image processing (PyMuPDF, Pillow). 3.9+ ensures `dict` union operators and type hint improvements are available without breaking compatibility with common system Python versions.

---

## TD-002 — PDF Library: PyMuPDF (fitz) >=1.23.0

**Decision**: Use `PyMuPDF` for PDF parsing and page rasterization.

**Alternatives considered**:
- `pdf2image` (wraps Poppler — requires system binary)
- `pypdf` (no rasterization capability)
- `pdfplumber` (text extraction focused, not rasterization)

**Rationale**: PyMuPDF is self-contained (no system binary dependencies), significantly faster than Poppler-based tools, and provides direct `pixmap` → PIL conversion. Single `pip install pymupdf` with no OS-level setup.

---

## TD-003 — Image Library: Pillow >=10.0.0

**Decision**: Use `Pillow` for all image operations: RGBA compositing, text rendering, font loading, and PDF assembly.

**Alternatives considered**:
- `opencv-cv2` (heavier, C++ dependency, overkill for this use case)
- `wand` (wraps ImageMagick — system dependency)
- `aggdraw` (unmaintained)

**Rationale**: Pillow handles the entire image pipeline in one library — RGBA compositing, TTF font rendering via `ImageDraw`, and PDF assembly via `save_all=True`. Well-maintained, pure Python wheel available. Pillow 10.0+ resolves deprecated APIs used in older versions.

---

## TD-004 — Rasterization DPI: 200

**Decision**: Rasterize pages at 200 DPI.

**Alternatives considered**:
- 72 DPI (screen resolution — too low, visible pixelation)
- 150 DPI (acceptable quality but borderline for dense text)
- 300 DPI (print quality — 2× file size and processing time vs. 200 DPI)

**Rationale**: 200 DPI produces clean output for digital distribution (the primary use case) without the performance cost of 300 DPI. An A4 page at 200 DPI is ~1654×2339 px, which is sufficient for watermark readability and content legibility.

---

## TD-005 — Watermark Opacity: 80/255 (~31%)

**Decision**: Apply watermark text at alpha value 80 out of 255.

**Alternatives considered**:
- 50/255 (~20%) — too faint on light backgrounds
- 128/255 (50%) — too heavy, obscures content in some layouts
- 180/255 (~70%) — defeats the purpose of semi-transparency

**Rationale**: 31% opacity is the established sweet spot for professional watermarks: clearly visible when looking for it, non-distracting during normal reading, does not prevent reading of underlying content.

---

## TD-006 — Watermark Color: (64, 64, 64) Dark Gray

**Decision**: Use RGB `(64, 64, 64)` for watermark text.

**Alternatives considered**:
- Black `(0, 0, 0)` — too harsh, high contrast even at low opacity
- Red `(180, 0, 0)` — alarm connotation, inappropriate for general use
- Blue `(0, 0, 180)` — draws attention to itself rather than the document

**Rationale**: Dark gray is visually neutral and professional. It contrasts against white backgrounds (standard paper) while remaining unobtrusive. Avoids the harshness of pure black at the chosen opacity level.

---

## TD-007 — Watermark Angle: -45 Degrees

**Decision**: Rotate watermark text at -45 degrees (bottom-left to top-right diagonal).

**Alternatives considered**:
- +45 degrees (top-left to bottom-right)
- -30 degrees (shallower diagonal)
- Horizontal (0 degrees)

**Rationale**: -45 degrees is the universal standard for diagonal watermarks. It is immediately recognizable as a watermark (not accidentally placed text), covers the page efficiently with tiling, and does not favor any reading direction.

---

## TD-008 — Font Size Formula: `max(36, int(page_width_px * 0.04))`

**Decision**: Scale font size dynamically based on page width in pixels, with a 36px minimum.

**Alternatives considered**:
- Fixed 48px regardless of page size
- Fixed percentage without minimum (breaks on very small pages)
- User-configurable via CLI flag

**Rationale**: A fixed font size looks proportional on A4 but either too large or too small on non-standard page sizes (A3, Letter, custom). The 4% ratio produces ~66px on an A4 page at 200 DPI, which is legible and proportional. The 36px minimum ensures readability on small pages.

---

## TD-009 — Tiling Strategy: Full Oversized Canvas Rotation

**Decision**: Tile text onto an oversized canvas, rotate the full canvas, then crop the center to page dimensions.

**Alternatives considered**:
- Rotate each text glyph individually and place it (complex math, inconsistent spacing)
- Tile horizontal text, then rotate the entire overlay image with `expand=True` and crop
- Per-cell rotation using a small stamp image for each tile position

**Rationale**: The oversized canvas approach is the simplest correct implementation. By making the canvas large enough to contain the full diagonal (at least `sqrt(width² + height²)`), rotation never clips content, and a simple center crop recovers exactly the page dimensions. No complex trigonometry required.

---

## TD-010 — Architecture: Single File `watermark.py`

**Decision**: Implement as a single Python file with no package structure.

**Alternatives considered**:
- Package with `src/watermark/` layout (over-engineered for ~150 LOC)
- Separate modules: `cli.py`, `pipeline.py`, `overlay.py` (unnecessary abstraction at this scale)

**Rationale**: The entire tool is ~150 lines across 6 functions. A single file is easier to distribute, read, and understand. Module splitting adds cognitive overhead and import complexity with no benefit at this scope. If the tool grows significantly beyond MVP, refactoring into modules is straightforward.
