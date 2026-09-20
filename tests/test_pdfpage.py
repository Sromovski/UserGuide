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
