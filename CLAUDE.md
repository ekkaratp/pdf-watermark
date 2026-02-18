# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python CLI tool that adds diagonal watermarks to PDF files. The core flow: convert each PDF page to an image (prevents element extraction/editing), overlay tiled watermark text, then re-assemble into a watermarked PDF.

**Development Framework**: BMAD MVP (PRD → Architecture → Milestone). All planning docs live in `docs/`. When a milestone task is completed, mark it as done in the corresponding doc.

**Coding Philosophy**: Minimal but robust — bycdev-expert patterns, MVP scope, no speculative features.

## Key Behaviors

- **Input**: Two CLI arguments — PDF full path, watermark text string
- **Output**: Same filename with `_watermark.pdf` postfix (e.g., `report.pdf` → `report_watermark.pdf`)
- **Watermark standard**: Diagonal, tiled, semi-transparent — visible over content but not obscuring it
- **Page conversion**: Each page must be rasterized before watermarking to prevent element copy/edit

## Test File

`sample/test.pdf` — use this for all manual testing.

## Development Workflow

1. Follow milestones defined in `docs/` (PRD → Architecture → Milestone breakdown)
2. Mark each completed milestone item as done in the relevant doc before moving on
3. Choose stable, well-accepted Python libraries for PDF and image processing
