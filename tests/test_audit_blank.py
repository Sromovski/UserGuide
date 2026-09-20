import fitz

import audit_pdfs
from covers import catalogue, pdfpage


def test_a_truly_empty_page_is_still_blank(tmp_path):
    p = tmp_path / 'empty.pdf'
    doc = fitz.open()
    doc.new_page(width=612, height=792)
    doc.save(str(p))
    doc.close()
    _n, _meta, issues = audit_pdfs.audit(str(p))
    assert issues['blank'] == [1]


def test_an_image_only_page_is_not_blank(tmp_path):
    p = tmp_path / 'cover.pdf'
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    p.write_bytes(data)
    _n, _meta, issues = audit_pdfs.audit(str(p))
    assert 'blank' not in issues
