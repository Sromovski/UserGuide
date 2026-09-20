import io

import fitz

from covers import catalogue, pdfpage


def test_produces_a_single_letter_page():
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    doc = fitz.open(stream=data, filetype='pdf')
    assert doc.page_count == 1
    r = doc[0].rect
    assert round(r.width) == 612 and round(r.height) == 792
    doc.close()


def test_the_page_carries_a_full_bleed_image():
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    doc = fitz.open(stream=data, filetype='pdf')
    info = doc[0].get_image_info()
    assert len(info) == 1
    bbox = fitz.Rect(info[0]['bbox'])
    assert bbox.width >= 611 and bbox.height >= 791
    doc.close()


def test_the_page_has_no_text_spans_so_the_audit_cannot_flag_it():
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    doc = fitz.open(stream=data, filetype='pdf')
    assert doc[0].get_text().strip() == ''
    doc.close()


def test_every_sku_produces_a_valid_cover_pdf():
    failures = []
    for name, spec in catalogue.all_specs().items():
        data = pdfpage.cover_pdf_bytes(spec)
        doc = fitz.open(stream=data, filetype='pdf')
        if doc.page_count != 1:
            failures.append(name)
        doc.close()
    assert failures == []


def test_no_cover_pdf_clips_its_title_or_badge_at_the_page_edge():
    # The page was once produced by centre-cropping a square render, which threw
    # away 227px per side — exactly the band holding the right margin and badge.
    # Assert the design's own ink never reaches the trim edge.
    offenders = []
    for name, spec in catalogue.all_specs().items():
        doc = fitz.open(stream=pdfpage.cover_pdf_bytes(spec), filetype='pdf')
        pix = doc[0].get_pixmap(dpi=72)
        w, h = pix.width, pix.height
        band = max(4, int(w * 0.012))
        px = [spec.palette.title, spec.palette.badge_bg]
        for x in list(range(band)) + list(range(w - band, w)):
            for y in range(0, h, 3):
                c = pix.pixel(x, y)
                if any(abs(c[0] - t[0]) + abs(c[1] - t[1]) + abs(c[2] - t[2]) < 24
                       for t in px):
                    offenders.append('%s: ink at x=%d y=%d' % (name, x, y))
                    break
            if offenders and offenders[-1].startswith(name):
                break
        doc.close()
    assert offenders == [], '\n'.join(offenders)
