"""Turn a rendered cover into a one-page US Letter PDF.

The cover is rasterised deliberately. The page carries no text spans, so
audit_pdfs.py cannot flag it for the overflow bugs that have hit cover pages
four times in this project's history. The PDF cover and the Etsy/Gumroad
listing images are not pixel-identical — the PDF renders the 'letter' shape
and the listing images render 'square'/'wide'/'pin' — but they are the same
design, the same CoverSpec, drawn by the same renderer at a different aspect,
so they cannot drift into different designs the way two separate art assets
could.
"""
import io

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from covers import render

PAGE_W, PAGE_H = 612.0, 792.0
DPI = 200          # the 'letter' shape is 1700x2200px = 8.5x11in at 200 DPI
JPEG_QUALITY = 92


def cover_pdf_bytes(spec):
    img = render.render(spec, 'letter')

    raw = io.BytesIO()
    img.save(raw, format='JPEG', quality=JPEG_QUALITY, optimize=True)
    raw.seek(0)

    out = io.BytesIO()
    c = canvas.Canvas(out, pagesize=(PAGE_W, PAGE_H))
    c.drawImage(ImageReader(raw), 0, 0, width=PAGE_W, height=PAGE_H)
    c.showPage()
    c.save()
    return out.getvalue()
