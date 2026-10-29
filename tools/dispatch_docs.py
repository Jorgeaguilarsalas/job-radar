"""Dispatch document generator — CV + cover letter PDFs from a JSON spec.

Layout = Jorge's one-page two-column CV (ReportLab, standard Helvetica, ~6 KB, Drive-uploadable).
Contains NO personal data: contact details, experience and wording come from the JSON spec,
which Claude builds per JD following the JD protocol + cv-template (verified facts only).

Usage:  python3 dispatch_docs.py spec.json outdir/
Spec keys: name, contact[], links[[label,url]], tagline, summary, skills_header, skills[],
           tools[], languages[], education[[title,sub]], jobs[[company,dates,role,[bullets]]],
           section_labels{contact,links,tools,languages,education,experience},
           cover_letter{date_line, salutation, paragraphs[], closing} (optional),
           file_stem (e.g. "Jorge_Aguilar_CV_Geotab")
"""
import json, sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, SimpleDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, FrameBreak, Table, TableStyle)

NAVY, BLUE, GREY, TEXT, SIDE = (HexColor(c) for c in ("#12305a", "#2d6cdf", "#4a5568", "#1c2533", "#eef2f7"))
W, H = A4
SIDE_W = W * 0.30
F, FB, FI = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"

def x(t):
    """Plain text in, ReportLab-safe out. Allows <b>, <i>, <br/> only."""
    t = str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for a, b in (("&lt;b&gt;", "<b>"), ("&lt;/b&gt;", "</b>"), ("&lt;i&gt;", "<i>"), ("&lt;/i&gt;", "</i>"), ("&lt;br/&gt;", "<br/>")):
        t = t.replace(a, b)
    return t

def build_cv(spec, path):
    def bg(c, d):
        c.saveState(); c.setFillColor(SIDE); c.rect(0, 0, SIDE_W, H, stroke=0, fill=1); c.restoreState()
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0,
                          title=spec.get("pdf_title", spec["name"] + " - CV"), author=spec["name"])
    side = Frame(8*mm, 9*mm, SIDE_W - 13.5*mm, H - 21*mm, 0, 0, 0, 0, id="side")
    main = Frame(SIDE_W + 7.5*mm, 8*mm, W - SIDE_W - 16.5*mm, H - 19*mm, 0, 0, 0, 0, id="main")
    doc.addPageTemplates([PageTemplate(frames=[side, main], onPage=bg)])
    sh = ParagraphStyle("sh", fontName=FB, fontSize=7.8, textColor=NAVY, spaceBefore=9, spaceAfter=3)
    sp = ParagraphStyle("sp", fontName=F, fontSize=7.8, leading=9.6, textColor=TEXT, spaceAfter=1.5)
    sb = ParagraphStyle("sb", parent=sp, leftIndent=7, bulletIndent=0, bulletFontName=F, bulletColor=BLUE)
    eb = ParagraphStyle("eb", parent=sp, fontName=FB, spaceAfter=0)
    es = ParagraphStyle("es", parent=sp, fontSize=7.3, textColor=GREY, spaceAfter=4)
    h1 = ParagraphStyle("h1", fontName=FB, fontSize=24, leading=26, textColor=NAVY)
    tag = ParagraphStyle("tag", fontName=FB, fontSize=8.2, textColor=BLUE, spaceBefore=4, spaceAfter=7)
    summ = ParagraphStyle("summ", fontName=F, fontSize=8.7, leading=11.4, textColor=TEXT, spaceAfter=8)
    h2 = ParagraphStyle("h2", fontName=FB, fontSize=9.2, textColor=NAVY, spaceAfter=5)
    co = ParagraphStyle("co", fontName=FB, fontSize=9.3, textColor=NAVY, leading=11)
    dt = ParagraphStyle("dt", fontName=F, fontSize=7.8, textColor=GREY, alignment=2, leading=11)
    role = ParagraphStyle("role", fontName=FI, fontSize=8.4, textColor=HexColor("#2a3a52"), spaceBefore=1, spaceAfter=2.5)
    bl = ParagraphStyle("bl", fontName=F, fontSize=8.5, leading=10.8, textColor=TEXT, leftIndent=9, bulletIndent=1, spaceAfter=1.8)
    L = {"contact": "CONTACT", "links": "LINKS", "tools": "TOOLS & TECH", "languages": "LANGUAGES",
         "education": "EDUCATION", "experience": "EXPERIENCE"}
    L.update(spec.get("section_labels", {}))
    def rule(width):
        t = Table([[""]], colWidths=[width], rowHeights=[1]); t.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, -1), 1, BLUE)])); return t
    sw, mw = side._width, main._width
    S = []
    def sec(t, first=False):
        if not first: S.append(Spacer(1, 6))
        S.append(Paragraph(x(t), sh)); S.append(rule(sw)); S.append(Spacer(1, 3))
    sec(L["contact"], True)
    for t in spec["contact"]: S.append(Paragraph(x(t), sp))
    sec(L["links"])
    for label, url in spec.get("links", []): S.append(Paragraph(f'<link href="{url}">{x(label)}</link>', sp))
    sec(spec["skills_header"])
    for t in spec["skills"]: S.append(Paragraph(x(t), sb, bulletText="•"))
    sec(L["tools"])
    for t in spec["tools"]: S.append(Paragraph(x(t), sb, bulletText="•"))
    sec(L["languages"])
    for t in spec["languages"]: S.append(Paragraph(x(t), sp))
    sec(L["education"])
    for a, b in spec["education"]: S.append(Paragraph(x(a), eb)); S.append(Paragraph(x(b), es))
    S.append(FrameBreak())
    S += [Paragraph(x(spec["name"]), h1), Paragraph(x(spec["tagline"]), tag), Paragraph(x(spec["summary"]), summ),
          Paragraph(x(L["experience"]), h2), rule(mw), Spacer(1, 5)]
    for c, d, r, bs in spec["jobs"]:
        t = Table([[Paragraph(x(c), co), Paragraph(x(d), dt)]], colWidths=[mw*0.6, mw*0.4])
        t.setStyle(TableStyle([(k, (0, 0), (-1, -1), 0) for k in ("LEFTPADDING", "RIGHTPADDING", "TOPPADDING", "BOTTOMPADDING")]))
        S += [t, Paragraph(x(r), role)] + [Paragraph(x(b), bl, bulletText="•") for b in bs] + [Spacer(1, 6)]
    doc.build(S)

def build_cl(spec, path):
    cl = spec["cover_letter"]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=24*mm, rightMargin=24*mm, topMargin=22*mm, bottomMargin=20*mm,
                            title=spec["name"] + " - Cover Letter", author=spec["name"])
    h = ParagraphStyle("h", fontName=FB, fontSize=18, textColor=NAVY, leading=22)
    c = ParagraphStyle("c", fontName=F, fontSize=8.8, textColor=GREY, leading=12)
    b = ParagraphStyle("b", fontName=F, fontSize=10.2, textColor=TEXT, leading=14.6, spaceAfter=9)
    S = [Paragraph(x(spec["name"]), h), Paragraph(x(" · ".join(spec["contact"])), c), Spacer(1, 14),
         Paragraph(x(cl["date_line"]), c), Spacer(1, 14), Paragraph(x(cl["salutation"]), b)]
    S += [Paragraph(x(p), b) for p in cl["paragraphs"]]
    S.append(Paragraph(x(cl["closing"]).replace("\n", "<br/>"), b))
    doc.build(S)

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    stem = spec.get("file_stem", "CV")
    cv = os.path.join(out, stem + ".pdf"); build_cv(spec, cv); print(cv)
    if spec.get("cover_letter"):
        clp = os.path.join(out, stem.replace("_CV_", "_Cover_Letter_").replace("_Lebenslauf_", "_Anschreiben_") + ".pdf")
        if clp == cv: clp = os.path.join(out, stem + "_Cover_Letter.pdf")
        build_cl(spec, clp); print(clp)
