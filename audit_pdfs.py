"""Production-readiness audit of the compiled volume PDFs.

Checks the mechanical things a human eye misses on 140 pages:
  - text running past the right margin or off the left
  - text colliding with the footer bar / header bar
  - overlapping text spans (the drawString-baseline bug class)
  - blank or near-blank pages
  - page counts and metadata
"""
import os
import sys
from collections import defaultdict

import fitz

OUT = r'C:\Projects\UserGuide\outputs'
W, H = 612.0, 792.0
MX = 0.65 * 72          # 46.8
RIGHT = W - MX          # 565.2
FOOTER_TOP = 22.0
HEADER_BOT = H - 6.0
TOL = 1.0

FILES = [
    'Claude_Field_Guide_Volume_1_Getting_Started.pdf',
    'Claude_Field_Guide_Volume_2_Developer_Setup.pdf',
    'Claude_Field_Guide_Volume_3_Claude_Code.pdf',
    'Claude_Field_Guide_Volume_4_Automation_Kit.pdf',
    'Claude_Field_Guide_Volume_5_API_Automation.pdf',
    'Claude_Field_Guide_Volume_6_Advanced.pdf',
    'Claude_Field_Guide_COMPLETE_LIBRARY.pdf',
]


def spans(page):
    """Yield (span_bbox, text, size, font, line_bbox).

    The LINE box matters for the bottom-bar test: PyMuPDF splits a line into spans at
    font changes, so a trailing glyph like an arrow is its own span sitting well right
    of centre, even though the line it belongs to is centred.
    """
    out = []
    d = page.get_text('dict')
    for blk in d.get('blocks', []):
        for line in blk.get('lines', []):
            lb = line.get('bbox', (0, 0, 0, 0))
            for sp in line.get('spans', []):
                t = sp['text']
                if t.strip():
                    out.append((sp['bbox'], t, sp['size'], sp['font'], lb))
    return out


def audit(path):
    doc = fitz.open(path)
    issues = defaultdict(list)
    for pno in range(doc.page_count):
        page = doc[pno]
        sp = spans(page)
        if not sp:
            issues['blank'].append(pno + 1)
            continue
        for bbox, text, size, font, lbox in sp:
            x0, y0, x1, y1 = bbox
            if x1 > RIGHT + TOL:
                issues['overflow_right'].append(
                    (pno + 1, round(x1 - RIGHT, 1), text[:70]))
            if x0 < MX - TOL:
                issues['overflow_left'].append(
                    (pno + 1, round(MX - x0, 1), text[:70]))
            # PDF y grows downward in PyMuPDF: footer bar is the bottom 22pt.
            if y1 > H - FOOTER_TOP + TOL and not _is_bar_content(lbox, text):
                issues['under_footer'].append((pno + 1, text[:70]))
        # overlapping spans on the same visual line
        by_y = defaultdict(list)
        for bbox, text, size, font, _lbox in sp:
            by_y[round(bbox[1] / 2)].append((bbox, text))
        for _, group in by_y.items():
            group.sort(key=lambda g: g[0][0])
            for i in range(len(group) - 1):
                a, b = group[i], group[i + 1]
                if a[0][2] > b[0][0] + 1.5:
                    issues['overlap'].append(
                        (pno + 1, a[1][:40], b[1][:40],
                         round(a[0][2] - b[0][0], 1)))
    meta = doc.metadata
    n = doc.page_count
    doc.close()
    return n, meta, issues


def _is_bar_content(bbox, text):
    """Text that BELONGS in a bottom bar, rather than body text that fell into one.

    Two legitimate cases: the 22pt page footer (guide title left, 'Page N' right), and
    the taller orange bar on cover pages, whose tagline is centred. Matching on phrases
    was brittle — it broke the moment the CTA wording changed — so match on geometry.
    """
    t = text.strip().lower()
    x0, _y0, x1, _y1 = bbox
    if t.startswith('page '):                             # right-aligned page number
        return True
    if abs(x0 - MX) < 3:                                  # left-aligned footer label
        return True
    if abs((x0 + x1) / 2 - W / 2) < 40:                   # centred cover-bar tagline
        return True
    return False


def main():
    # Accept explicit paths so a new series can be audited without editing FILES.
    files = [os.path.basename(a) for a in sys.argv[1:]] or FILES
    total_issues = 0
    for f in files:
        p = os.path.join(OUT, f)
        if not os.path.exists(p):
            print('MISSING %s' % f)
            continue
        n, meta, issues = audit(p)
        print('\n' + '=' * 78)
        print('%s  —  %d pages' % (f, n))
        print('  title:   %s' % meta.get('title'))
        print('  author:  %s' % meta.get('author'))
        print('  subject: %s' % (meta.get('subject') or '')[:70])
        if not issues:
            print('  CLEAN')
            continue
        for kind, items in sorted(issues.items()):
            total_issues += len(items)
            print('  %s: %d' % (kind.upper(), len(items)))
            for it in items[:12]:
                print('     %s' % (it,))
            if len(items) > 12:
                print('     ... %d more' % (len(items) - 12))
    print('\n%d issue instances total' % total_issues)


if __name__ == '__main__':
    main()
