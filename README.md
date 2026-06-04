# en-bn-ocr-tool
> Turns Bengali and English images into structured Markdown notes. Tesseract under the hood, Obsidian in mind.

A desktop OCR tool that extracts text from images containing Bengali and/or English script, cleans the output, and saves it as formatted Markdown — with optional direct export to an Obsidian vault.

---

## Stack

- Python 3.12
- Tesseract OCR via `pytesseract` — Bengali (`ben`) + English (`eng`) language packs
- OpenCV (`cv2`) — image preprocessing (grayscale, denoising, deskew, thresholding)
- Pillow — PIL image handling
- Tkinter — desktop GUI
- Regex-based Markdown conversion — no external parser

---

## Structure

```
en-bn-ocr-tool/
├── main.py               # Entry point — launches GUI or test runner
├── ocr_engine.py         # Image preprocessing + Tesseract OCR
├── markdown_converter.py # Raw text → structured Markdown with YAML frontmatter
├── file_handler.py       # Saves .md files, handles batch folder processing
├── gui_app.py            # Tkinter desktop interface
├── full_test.py          # End-to-end test runner
├── test_installation.py  # Dependency check
├── test_ocr.py           # OCR unit test
└── test_markdown.py      # Markdown conversion test
```

---

## Pipeline

```
Image → Preprocess → OCR → Convert → Save
```

1. **Preprocess** — grayscale, denoise, Otsu threshold, auto-deskew
2. **OCR** — Tesseract with `--oem 3 --psm 6`, Bengali + English by default
3. **Convert** — pattern-match lines into headings, lists, bullets; wrap in YAML frontmatter
4. **Save** — timestamped `.md` file into `OCR_Notes/`, or directly into an Obsidian vault

---

## Requirements

Install Python dependencies:

```bash
pip install pytesseract opencv-python pillow numpy
```

Install Tesseract and the Bengali language pack:

- **Windows:** [Tesseract installer](https://github.com/tesseract-ocr/tesseract/releases) — include Bengali during setup
- **macOS:** `brew install tesseract tesseract-lang`
- **Linux:** `sudo apt install tesseract-ocr tesseract-ocr-ben`

> **Windows note:** The Tesseract path is currently hardcoded to `C:\Program Files\Tesseract-OCR\tesseract.exe` in `ocr_engine.py`. Adjust if your install path differs.

---

## Usage

**Launch the GUI:**

```bash
python main.py
```

**Run the end-to-end test** (requires a test image at `test_bengali_note.jpg`):

```bash
python main.py --test
```

**Supported image formats:** `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`

---

## Output

Each processed image produces a `.md` file with YAML frontmatter:

```markdown
---
title: extracted or inferred title
created: 2025-05-29 15:30
tags: [notes, ocr]
---

## Heading detected from text

1. Numbered item
- Bullet point
Regular paragraph text...
```

Files are saved to `OCR_Notes/` by default, or to `<vault>/OCR_Notes/` if an Obsidian vault path is provided.

---

## Known Limitations

- Tesseract path is hardcoded for Windows — needs manual adjustment on other platforms
- No PDF input support — images only
- Header detection is broad and may promote regular sentences to headings
- `0 → O` substitution in cleanup can corrupt numeric content

---

## License

MIT
