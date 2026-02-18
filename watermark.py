"""
watermark.py — Add diagonal tiled watermarks to PDF files.

Usage: python watermark.py <pdf_path> <watermark_text>
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

DPI = 200
WATERMARK_OPACITY = 25  # 25 % of 255
WATERMARK_COLOR = (64, 64, 64)
WATERMARK_ANGLE = -45
FONT_SIZE_RATIO = 0.04
FONT_SIZE_MIN = 36
TILE_PADDING = 120


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def validate_inputs(pdf_path: str, watermark_text: str) -> None:
    """Validate that pdf_path exists, is a PDF, and watermark_text is non-empty."""
    path = Path(pdf_path)
    if not path.exists():
        print(f"Error: file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    if path.suffix.lower() != ".pdf":
        print(f"Error: not a PDF file: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    if not watermark_text.strip():
        print("Error: watermark text must not be empty.", file=sys.stderr)
        sys.exit(1)


def rasterize_page(page) -> Image.Image:
    """Render a fitz Page to a PIL RGBA Image at DPI resolution."""
    matrix = fitz.Matrix(DPI / 72, DPI / 72)
    pix = page.get_pixmap(matrix=matrix, alpha=True)
    img = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    return Image.alpha_composite(white, img)


def make_watermark_overlay(width: int, height: int, text: str) -> Image.Image:
    """Create a transparent RGBA image with tiled diagonal watermark text.

    Strategy: tile text on an oversized square canvas (side = page diagonal),
    rotate the whole canvas by WATERMARK_ANGLE, then crop the centre to
    (width, height).  The oversized canvas ensures rotation never clips content.
    """
    font_size = max(FONT_SIZE_MIN, int(width * FONT_SIZE_RATIO))
    for face in ("Arial Bold.ttf", "Arial.ttf"):
        try:
            font = ImageFont.truetype(face, font_size)
            break
        except (IOError, OSError):
            continue
    else:
        font = ImageFont.load_default(size=font_size)

    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Oversized canvas: diagonal length guarantees no corner clipping after rotation.
    diag = math.ceil(math.sqrt(width ** 2 + height ** 2))
    canvas = Image.new("RGBA", (diag, diag), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    fill = WATERMARK_COLOR + (WATERMARK_OPACITY,)
    step_x = text_w + TILE_PADDING
    step_y = text_h + TILE_PADDING

    for y in range(0, diag, step_y):
        for x in range(0, diag, step_x):
            draw.text((x, y), text, font=font, fill=fill)

    rotated = canvas.rotate(WATERMARK_ANGLE, expand=False)

    left = (diag - width) // 2
    top = (diag - height) // 2
    return rotated.crop((left, top, left + width, top + height))


def apply_watermark(page_img: Image.Image, overlay: Image.Image) -> Image.Image:
    """Composite the RGBA overlay onto the RGBA page image; return RGB."""
    composited = Image.alpha_composite(page_img, overlay)
    return composited.convert("RGB")


def build_output_path(pdf_path: str) -> str:
    """Return the output path: same dir/name as pdf_path with _watermark suffix."""
    p = Path(pdf_path)
    return str(p.parent / f"{p.stem}_watermark.pdf")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add a diagonal tiled watermark to every page of a PDF."
    )
    parser.add_argument("pdf_path", help="Path to the input PDF file.")
    parser.add_argument("watermark_text", help="Text to use as the watermark.")
    args = parser.parse_args()

    validate_inputs(args.pdf_path, args.watermark_text)

    doc = fitz.open(args.pdf_path)
    output_pages: list[Image.Image] = []

    for page in doc:
        page_img = rasterize_page(page)
        overlay = make_watermark_overlay(page_img.width, page_img.height, args.watermark_text)
        output_pages.append(apply_watermark(page_img, overlay))

    doc.close()

    output_path = build_output_path(args.pdf_path)
    output_pages[0].save(
        output_path,
        save_all=True,
        append_images=output_pages[1:],
    )
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
