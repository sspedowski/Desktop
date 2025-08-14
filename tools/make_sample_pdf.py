from reportlab.pdfgen import canvas
from pathlib import Path

out_dir = Path("data/input/pdfs")
out_dir.mkdir(parents=True, exist_ok=True)
pdf_path = out_dir / "sample.pdf"

c = canvas.Canvas(str(pdf_path))
c.setFont("Helvetica", 16)
c.drawString(72, 720, "Justice File Sample PDF")
c.setFont("Helvetica", 12)
c.drawString(72, 700, "This is a sample PDF for pipeline testing.")
c.save()

print(f"Sample PDF created at {pdf_path}")
