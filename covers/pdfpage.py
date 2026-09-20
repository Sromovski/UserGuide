"""Turn a rendered cover into a one-page US Letter PDF.

The cover is rasterised deliberately. One engine draws both the listing image
and the PDF cover page, so they cannot drift; and because the page carries no
text spans, audit_pdfs.py cannot flag it for the overflow bugs that have hit
cover pages four times in this project's history.
"""
import io

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from covers import render

PAGE_W, PAGE_H = 612.0, 792.0
DPI = 200
JPEG_QUALITY = 92


def _letter_crop(img):
    """Centre-crop the square render to the page aspect. Never distort."""
    target = PAGE_W / PAGE_H
    w, h = img.size
    new_h = int(round(w / target))
    if new_h > h:                      # too tall for the source: crop width
        new_w = int(round(h * target))
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    top = (h - new_h) // 2
    return img.crop((0, top, w, top + new_h))


def cover_pdf_bytes(spec):
    img = _letter_crop(render.render(spec, 'square'))
    target_px = (int(PAGE_W / 72.0 * DPI), int(PAGE_H / 72.0 * DPI))
    img = img.resize(target_px, Image.LANCZOS)

    raw = io.BytesIO()
    img.save(raw, format='JPEG', quality=JPEG_QUALITY, optimize=True)
    raw.seek(0)

    out = io.BytesIO()
    c = canvas.Canvas(out, pagesize=(PAGE_W, PAGE_H))
    c.drawImage(ImageReader(raw), 0, 0, width=PAGE_W, height=PAGE_H)
    c.showPage()
    c.save()
    return out.getvalue()
