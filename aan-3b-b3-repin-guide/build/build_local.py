#!/usr/bin/env python3
import json, argparse, pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors

def header_bar(c, title, spec):
    hb = spec["styling"]["header_bar"]
    c.setFillColor(colors.HexColor(hb["color_hex"]))
    c.rect(0, 10.5*inch, 8.5*inch, hb["height_in"]*inch, fill=1, stroke=0)
    c.setFillColor(colors.HexColor(hb["text_color_hex"]))
    c.setFont(spec["styling"]["font_heading"], 12)
    c.drawString(0.75*inch, 10.5*inch + 0.12*inch, title.upper())

def footer_page_num(c, num_str):
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#9e9e9e"))
    c.drawCentredString(4.25*inch, 0.5*inch, num_str)

def table_with_check(c, df, title, spec):
    header_bar(c, title, spec)
    y = 10*inch
    # header
    c.setFont("Helvetica-Bold",8)
    cols = list(df.columns) + ["Verified"]
    widths = [0.6,0.6,1.3,0.6,1.2,0.7,0.7,1.0,1.2,0.4] if len(df.columns)==9 else [ (7.5/len(cols))*inch for _ in cols ]
    x = 0.6*inch
    for i,col in enumerate(cols):
        if isinstance(widths[0], float): # list of floats (already in inches)
            w = widths[i] if i < len(widths) else 0.7*inch
        else:
            w = widths[i]
        c.drawString(x+2, y, str(col)); x += w
    y -= 12
    c.setFont("Helvetica",8)
    # rows
    for _,row in df.iterrows():
        x = 0.6*inch
        for i,col in enumerate(cols[:-1]):
            txt = str(row.get(col, ""))[:34]
            if isinstance(widths[0], float):
                w = widths[i] if i < len(widths) else 0.7*inch
            else:
                w = widths[i]
            c.drawString(x+2, y, txt); x += w
        c.rect(x+2, y-2, 8, 8, fill=0, stroke=1)
        y -= 12
        if y < 1.0*inch:
            c.showPage()
            header_bar(c, title + " (cont.)", spec)
            y = 10*inch
            c.setFont("Helvetica-Bold",8)
            x = 0.6*inch
            for i,col in enumerate(cols):
                if isinstance(widths[0], float):
                    w = widths[i] if i < len(widths) else 0.7*inch
                else:
                    w = widths[i]
                c.drawString(x+2, y, str(col)); x += w
            y -= 12; c.setFont("Helvetica",8)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    args = ap.parse_args()

    with open(args.spec, "r", encoding="utf-8") as f:
        spec = json.load(f)

    xlsx = spec["inputs"]["xlsx_path"]
    out_pdf = spec["inputs"]["pdf_output"]

    # Load whatever exists
    def safe_read(sheet):
        try:
            return pd.read_excel(xlsx, sheet_name=sheet)
        except Exception:
            return pd.DataFrame()

    pin = safe_read("Pin Mapping")
    views = safe_read("Connector Views")
    steps = safe_read("Steps")
    diag = safe_read("Diagnostics")
    colors_sheet = safe_read("Color Key")
    sources = safe_read("Sources")

    c = canvas.Canvas(out_pdf, pagesize=letter)
    W,H = letter

    # Cover
    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.75*inch, H-1.2*inch, spec["title"])
    c.setFont("Helvetica", 11)
    c.drawString(0.75*inch, H-1.5*inch, f'{spec["revision"]} — {spec["revision_date"]} • {spec["author"]} • {spec["license"]} License')
    c.showPage()

    # Publication Data
    header_bar(c, "Publication Data & Revision Index", spec)
    c.setFont("Helvetica", 10)
    y = 10*inch
    for k,v in [("Document Title", spec["title"]),
                ("Author", spec["author"]),
                ("Revision", f'{spec["revision"]} — {spec["revision_date"]}'),
                ("License", spec["license"]),
                ("Repository", "github.com/dspl1236/Audi/aan-3b-b3-repin-guide")]:
        c.drawString(0.75*inch, y, f"{k}: {v}"); y -= 14
    c.showPage()

    # TOC (static)
    header_bar(c, "Table of Contents", spec)
    c.setFont("Helvetica", 10)
    y = 10*inch
    for line in ["1  Introduction & Overview",
                 "2  ECU T55 Pin Mapping",
                 "3  Connector Views (T6a/T6b/T8a/T8b)",
                 "4  B3 7A Integration",
                 "5  Diagnostics & MIL",
                 "6  Wire Color Reference",
                 "7  Sources & Credits",
                 "Appendix A  AAN ECU (Motronic 2.3.2)",
                 "Appendix B  3B ECU (Motronic 2.3.1)",
                 "Appendix C  B3 7A Integration Map",
                 "Appendix D  Master Cross-Reference"]:
        c.drawString(0.75*inch, y, line); y -= 16
    c.showPage()

    # Intro
    header_bar(c, "Introduction & Overview", spec)
    c.setFont("Helvetica", 10)
    y = 10*inch
    for L in [
        "Convert AAN harness to 3B ECU in B3 7A chassis.",
        "Includes mappings, connector views, diagnostics, and verification checkboxes."
    ]:
        c.drawString(0.75*inch, y, L); y -= 14
    c.showPage()

    # ECU T55
    table_with_check(c, pin, "ECU T55 Pin Mapping", spec); c.showPage()

    # Connector Views
    if not views.empty:
        table_with_check(c, views, "Connector Views", spec); c.showPage()

    # Integration
    if not steps.empty:
        table_with_check(c, steps, "B3 7A Integration", spec); c.showPage()

    # Diagnostics
    if not diag.empty:
        table_with_check(c, diag, "Diagnostics & MIL", spec); c.showPage()

    # Wire Colors
    if not colors_sheet.empty:
        table_with_check(c, colors_sheet, "Wire Color Reference", spec); c.showPage()

    # Sources
    if not sources.empty:
        table_with_check(c, sources, "Sources & Credits", spec); c.showPage()

    # Appendices (placeholders)
    for title in ["Appendix A – AAN ECU (Motronic 2.3.2)",
                  "Appendix B – 3B ECU (Motronic 2.3.1)",
                  "Appendix C – B3 7A Integration Map",
                  "Appendix D – Master Cross-Reference"]:
        header_bar(c, title, spec)
        footer_page_num(c, "Page — of —")  # minimal numbering
        c.setFont("Helvetica",10)
        c.drawString(0.75*inch, 10*inch, "See reference tables in workbook or mapped sections above.")
        c.showPage()

    # Back cover
    c.setFont("Helvetica",10)
    c.drawString(0.75*inch, 6.0*inch, "Compiled & illustrated by Andrew Schlueter — MIT License")
    c.drawString(0.75*inch, 5.8*inch, "Source: github.com/dspl1236/Audi")
    c.save()

if __name__ == "__main__":
    main()
