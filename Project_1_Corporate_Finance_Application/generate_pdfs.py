"""Create reviewable PDF versions of the three written evidence surfaces."""
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).parent
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawString(.65 * inch, .45 * inch, "FIN 43900 - Project 1 - Eli Lilly (LLY)")
    canvas.drawRightString(7.85 * inch, .45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def md_to_pdf(source: str, output: str, title: str):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12, spaceAfter=6))
    styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17, leading=21, spaceBefore=4, spaceAfter=10))
    styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=15, spaceBefore=10, spaceAfter=5))
    story = [Paragraph(title, styles["Title"]), Spacer(1, 8)]
    for raw in (ROOT / source).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("|---"):
            continue
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        line = line.replace("**", "")
        if line.startswith("# "):
            story.append(Paragraph(line[2:], styles["H1x"]))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], styles["H2x"]))
        elif line.startswith("| "):
            story.append(Paragraph(line.strip("|").replace("|", " &nbsp; | &nbsp; "), styles["Body"]))
        elif line.startswith("- "):
            story.append(Paragraph("- " + line[2:], styles["Body"]))
        else:
            story.append(Paragraph(line.replace("`", ""), styles["Body"]))
    SimpleDocTemplate(str(OUT / output), pagesize=letter, leftMargin=.65*inch, rightMargin=.65*inch, topMargin=.6*inch, bottomMargin=.7*inch).build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    md_to_pdf("MEMO.md", "LLY_Committee_Memo.pdf", "Eli Lilly Committee Memo")
    md_to_pdf("VALIDATION_AND_AI_USE.md", "LLY_Validation_and_AI_Use.pdf", "LLY Validation and AI Use Record")
    md_to_pdf("RESEARCH_EVOLUTION.md", "LLY_Research_Evolution.pdf", "LLY Research Evolution")
