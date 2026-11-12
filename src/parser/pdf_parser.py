import fitz

RENDER_DPI = 400


def render_pdf(path):
    with fitz.open(path) as doc:
        return [page.get_pixmap(dpi=RENDER_DPI, alpha=False).tobytes("png") for page in doc]
